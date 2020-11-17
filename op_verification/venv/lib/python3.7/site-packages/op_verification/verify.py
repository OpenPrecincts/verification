# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 15:23:41 2020

@author: baxterdemers
"""
#%%
import pandas as pd
import geopandas as gpd
import warnings
from functools import reduce
from operator import add
import statistics

from gerrychain import Graph
import maup
import shapely as shp
from collections import defaultdict

from verification_data import expected_election_results_2016, census_us_county_gdf
from reference_data import (
    geoid_to_county_name,
    state_to_fips,
    state_abbreviation_to_state_name,
)


class Election:
    def __init__(self, results_df):
        self.n_votes_democrat_expected = results_df[results_df.party == "democrat"][
            "votes"
        ].sum()
        self.n_votes_republican_expected = results_df[results_df.party == "republican"][
            "votes"
        ].sum()
        self.n_two_party_votes_expected = (
            self.n_votes_democrat_expected + self.n_votes_republican_expected
        )


class ElectionReport(Election):
    def __init__(self, results_df, shp_df, d_col="d_col", r_col="r_col"):
        Election.__init__(self, results_df)
        shp_df = self.remove_commas(shp_df, [d_col, r_col])
        self.n_votes_democrat_observed = shp_df[d_col].sum()
        self.n_votes_republican_observed = shp_df[r_col].sum()
        self.n_two_party_votes_observed = (
            self.n_votes_democrat_observed + self.n_votes_republican_observed
        )
        self.vote_score = self.compute_vote_score(
            self.n_votes_democrat_observed,
            self.n_votes_republican_observed,
            self.n_votes_democrat_expected,
            self.n_votes_republican_expected,
        )

    def remove_commas(self, df, col_lst):
        """
        remove commas from the string representation of numbers in the cols in col_lst

        :df: DataFrame object
        :col_lst: list of strings that are each the name of a column :df:
        """
        for col in col_lst:
            if df.dtypes[col] == "object":
                df[col] = df[col].map(lambda s: s.replace(",", ""))
            df = df.astype({col: "float"})
            df = df.astype({col: "int64"})
        return df

    def compute_vote_score(
        self,
        n_votes_democrat_observed,
        n_votes_republican_observed,
        n_votes_democrat_expected,
        n_votes_republican_expected,
    ):
        """
        return vote score (float)

        :n_votes_democrat_observed: (int)
        :n_votes_republican_observed: (int)
        :n_votes_democrat_expected: (int)
        :n_votes_republican_expected: (int)

        Compute the ratio of votes observed in the **Input** to the votes expected
        (based on official state election data records from MEDSL) for the democratic
        and republican candidate. Then the Vote Score is the weighted average of
        these ratios. Check out the README for more information.
        """
        n_two_party_votes_expected = (
            n_votes_democrat_expected + n_votes_republican_expected
        )
        dem_vote_ratio = n_votes_democrat_observed / n_votes_democrat_expected
        rep_vote_ratio = n_votes_republican_observed / n_votes_republican_expected
        return (
            (dem_vote_ratio * n_votes_democrat_expected)
            + (rep_vote_ratio * n_votes_republican_expected)
        ) / n_two_party_votes_expected

    def get_squared_diff(self):
        squared_diff = (
            self.n_two_party_votes_expected - self.n_two_party_votes_observed
        ) ** 2
        return squared_diff


class CountyReport(ElectionReport):
    def __init__(self, results_df, shp_df, area_difference_score, geoid):
        ElectionReport.__init__(self, results_df, shp_df)
        self.geoid = geoid
        self.name = (
            geoid_to_county_name[geoid]
            if geoid[0:2] != "02"
            else "District " + geoid[3:]
        )
        self.area_difference_score = area_difference_score

    def __str__(self):
        return "{} County (GEOID = {})".format(self.name, self.geoid)


class State:
    def __init__(self, state_abbreviation):
        self.abbreviation = state_abbreviation
        self.name = state_abbreviation_to_state_name[state_abbreviation]
        self.fips = str(state_to_fips[self.name]).zfill(2)

    def __str__(self):
        return "{} (State FIPS = {})".format(self.name, self.fips)


class StateReport(ElectionReport, State):
    def __init__(
        self,
        results_df,
        shp_df,
        state_abbreviation,
        year,
        source,
        office,
        all_precincts_have_a_geometry=False,
        can_use_maup=False,
        can_use_gerrychain=False,
        county_vote_score_dispersion=-1,
        worst_county_area_difference_score=-1,
        worst_county_vote_score=-1,
        median_county_area_difference_score=-1,
    ):
        State.__init__(self, state_abbreviation)
        ElectionReport.__init__(self, results_df, shp_df)
        self.county_vote_score_dispersion = county_vote_score_dispersion
        self.worst_county_vote_score = worst_county_vote_score
        self.median_county_area_difference_score = median_county_area_difference_score
        self.worst_county_area_difference_score = worst_county_area_difference_score
        # Election Map Attributes
        self.year = year
        self.source = source
        self.office = office
        # Topology Checks
        self.all_precincts_have_a_geometry = all_precincts_have_a_geometry
        self.can_use_maup = can_use_maup
        self.can_use_gerrychain = can_use_gerrychain

    def __str__(self):
        return "{} {} by {}".format(self.year, self.abbreviation, self.source)


def fix_buffer(gdf):
    """
    return (GeoDataFrame) with the 'bufer(0) trick' applied

    :gdf: (GeoDataFrame) object

    Can be useful when trying to mitigate 'self-intersection' issues
    """
    buffered = gdf.buffer(0)
    gdf.drop(columns=["geometry"])
    # gdf['geometry'] = gdf.apply(lambda x: x.geometry.buffer(0), axis=1)
    gdf["geometry"] = buffered
    return gdf


def get_area_difference_score(gdf1, gdf2, path=None):
    """
    Return the Area Difference Score with respect to gdf1

    :gdf1: (GeoDataFrame)
    :gdf2: (GeoDataFrame)
    :path: (str) representing the file path where a shapefile of the diff should be saved

    Compute the symmetric difference between gdf1 and gdf2 geometries'.
    The Area Difference Score is the ratio of the symmetric difference's area to the
    area of the precinct shapefiles. Check out the README for more information.

    Optionally, to save a shapefile of the symmetric difference provide an arguement
    for the path parameter.
    """
    try:
        if not gdf1.crs:
            gdf1.crs = "epsg:4326"
        gdf1 = gdf1.to_crs(gdf2.crs)
        poly1 = shp.ops.cascaded_union(gdf1["geometry"])
        poly2 = shp.ops.cascaded_union(gdf2["geometry"])

        valid = poly1.area > 0 and poly2.area > 0
        if not valid:
            print("invalid")
            return -1

        diff = poly2.symmetric_difference(poly1)
        diff_area = diff.area
        if path:
            gdf = gpd.GeoSeries(diff)
            gdf.to_file("exports/shapefile-diffs/" + path)
        return diff_area / poly1.area
    except Exception as err:
        print("Unable to compare area - ", err)
        return -1


def get_column_name(target, potential_column_names, gdf):
    """
    return name from potential_column_names based on user input

    :target: (str) what the user should find e.g. County
    :potential_column_names: ((str) list) of potential column names
    :gdf: (GeoDataFrame) containing the columns being reviewed

    Raises Exception when no valid column is found
    """
    print("Please manually select the {} column by index: ".format(target))
    potential_column_names = list(potential_column_names)
    for idx, column_name in enumerate(potential_column_names):
        print("[{}] {} e.g. {}".format(idx, column_name, gdf[column_name][0]))
    print("[{}] N/A (no suitable match for {})".format(idx + 1, target))
    idx_selection = int(input("Select the column (by index): "))
    if 0 <= idx_selection <= idx:
        return potential_column_names[idx_selection]
    else:
        raise Exception("Unable to find a suitable column")


def get_closest_column(target_value, target_name, col_to_value, gdf, stopping_words=[]):
    """
    return the name of the column closet to the 'target_value' (str)

    :target_value: (int) the ideal value for the column to have from applying an aggfunc
    :target_name: (str) the name of the target column
    :col_to_value: ({(str):(int)}) dictionary mapping column name to column value
    :gdf: (GeoDataFrame) containing the columns being reviewed
    :stopping_words: ((str) list)

    If a stopping word is in a column name then that column name will be returned.
    Ignores case. Stopping words should be in descending order of relavence.

    If there are two choices that seem equally good, the user will be prompted for input
    """
    col_to_diff = {
        col: abs(value - target_value) for col, value in col_to_value.items()
    }
    min_diff = min(col_to_diff.values())
    potential_columns = [col for col, diff in col_to_diff.items() if diff == min_diff]
    if len(potential_columns) == 1:
        return potential_columns[0]
    elif len(potential_columns) > 1:
        if stopping_words:
            for col in potential_columns:
                for stopping_word in stopping_words:
                    if stopping_word.lower() in col.lower():
                        return col
        get_column_name(target_name, potential_columns, gdf)
    else:
        raise Exception("Unable to find a county col")


def get_party_cols(gdf, state_abbreviation):
    """
    return d_col and r_col for 2016, will prompt user if unsure. (str, str)

    :gdf: (GeoDataFrame) containing precinct level election results
    :state_abbreviation: (str) e.g. 'MA'
    """
    results_df = expected_election_results_2016[
        expected_election_results_2016.state_po == state_abbreviation
    ]
    election = Election(results_df)

    col_to_value = {
        col: gdf[col].sum()
        for col in gdf.select_dtypes(include="number").columns
        if "16" in col and "p" in col.lower()
    }

    d_col = get_closest_column(
        election.n_votes_democrat_expected,
        "democratic presidential votes",
        col_to_value,
        gdf,
    )
    r_col = get_closest_column(
        election.n_votes_republican_expected,
        "republican presidential votes",
        col_to_value,
        gdf,
    )

    if d_col == r_col:
        d_col = get_column_name("Democrat candidate votes", col_to_value.keys(), gdf)
        r_col = get_column_name("Republican candidate votes", col_to_value.keys(), gdf)
    assert d_col != r_col
    return d_col, r_col


def assign_GEOID(state_prec_gdf, state_fips):
    """
    return the (GeoDataFrame) with a column 'GEOID' indicating a precinct's county

    :state_prec_gdf: (GeoDataFrame) with statewide precinct level election results
    :state_fips: (int) Federal Information Processing Standard state code

    returned GeoDataFrame's 'GEOID' column will conform to the GEOID spec:

    Elements of the GEOID column are 5 character strings. The first 2 characters
    are the StateFP code and the last 3 characters are the CountyFP code. e.g.

    Massachusetts' StateFP = '25'
    Essex County's CountyFP = '009'
    Essex County, Massachusetts' GEODID = '25009'

    If either code has fewer digits than are allocated, the string representation should
    be zero-padded from the left. e.g. Alaska (StateFP = 2) should be '02'.
    """
    state_fips_str = str(state_fips).zfill(2)
    state_county_df = census_us_county_gdf[
        census_us_county_gdf["STATEFP"] == state_fips_str
    ]
    # match their projections (necessary for maup.assign)
    if not state_prec_gdf.crs:
        state_prec_gdf.crs = "epsg:4326"
    state_prec_gdf = state_prec_gdf.to_crs(state_county_df.crs)
    assert state_prec_gdf.crs == state_county_df.crs

    state_prec_gdf["maup_assignment"] = maup.assign(
        fix_buffer(state_prec_gdf), state_county_df
    )
    state_prec_gdf["GEOID"] = state_prec_gdf["maup_assignment"].map(
        lambda idx: state_fips_str + str(state_county_df.loc[idx]["COUNTYFP"]).zfill(3)
    )
    n_counties_observed = state_prec_gdf["GEOID"].nunique()
    n_counties_expected = state_county_df["GEOID"].nunique()
    assert n_counties_expected == n_counties_observed
    return state_prec_gdf


def verify_counties(gdf, county_level_results_df, state_report):
    """
    returns ((ElectionReport) list) for all counties and County Vote Score Dispersion (float)

    :gdf: (GeoDataFrame) containing the statewide shapefile with election results
    :county_level_results_df: (DataFrame) rows = votes for one party's candidate per county
    :state_report: (StateReport) instance for the statewide election

    Expects the first two arguements to have a column 'GEOID'. Elements
    of the GEOID column are 5 character strings. The first 2 characters are the StateFP
    code and the last 3 characters are the CountyFP code. e.g.

    Massachusetts' StateFP = '25'
    Essex County's CountyFP = '009'
    Essex County, Massachusetts' GEODID = '25009'

    If either code has fewer digits than are allocated, the string representation should
    be zero-padded from the left. e.g. Alaska (StateFP = 2) should be '02'.
    """

    def get_worst_area_diff(county_reports):
        """
        return worst area diff for a iterable containting county reports

        :county_reports: CountyReport list
        -1 is the worst (indicates an error - likely missing a county)
        otherwise a higher number is worse (greater difference)
        """
        diff_set = set(map(lambda x: x.area_difference_score, county_reports))
        if -1 in diff_set:
            return -1
        else:
            return max(diff_set)

    # verify preconditions:
    assert {"GEOID", "geometry"}.issubset(set(gdf.columns))
    assert {"county", "GEOID", "party", "votes"}.issubset(
        set(county_level_results_df.columns)
    )
    for sample_geoid in {gdf["GEOID"][0], county_level_results_df["GEOID"][0]}:
        assert type(sample_geoid) == str and len(sample_geoid) == 5

    results_county_GEOID_set = set(county_level_results_df["GEOID"].unique())
    n_counties = len(results_county_GEOID_set)
    assert n_counties == gdf["GEOID"].nunique()

    # get county-level expected geometries for the state
    state_county_gdf_census = census_us_county_gdf[
        census_us_county_gdf["STATEFP"] == state_report.fips
    ]

    # initialize loop variables
    n_matches = 0
    county_reports = []

    for shp_county_GEOID in gdf["GEOID"].unique():
        if shp_county_GEOID in results_county_GEOID_set:
            n_matches += 1

            # get county specific (Geo)DataFrames
            county_gdf_shp = gdf[gdf["GEOID"] == shp_county_GEOID]
            county_df_expected_results = county_level_results_df[
                county_level_results_df["GEOID"] == shp_county_GEOID
            ]
            county_gdf_expected_geometries = state_county_gdf_census[
                state_county_gdf_census["GEOID"] == shp_county_GEOID
            ]

            area_difference_score = get_area_difference_score(
                county_gdf_shp, county_gdf_expected_geometries
            )
            county_report = CountyReport(
                county_df_expected_results,
                county_gdf_shp,
                area_difference_score,
                shp_county_GEOID,
            )
            county_reports.append(county_report)

        else:
            print(
                "GEOID={} (Name = {}) is NOT in `county_level_results_df`".format(
                    shp_county_GEOID,
                    geoid_to_county_name.get(shp_county_GEOID, "UNKNOWN"),
                )
            )

    # test for full coverage
    county_coverage = (
        reduce(add, map(lambda x: x.n_two_party_votes_observed, county_reports))
        / state_report.n_two_party_votes_observed
    )
    assert county_coverage == 1
    assert n_matches == n_counties

    # compute measures for the state_report comparing all the counties
    state_report.county_vote_score_dispersion = (
        reduce(add, map(lambda x: x.get_squared_diff(), county_reports)) / n_counties
    )
    state_report.worst_county_vote_score = reduce(
        lambda a, b: a if abs(a - 1) > abs(b - 1) else b,
        map(lambda x: x.vote_score, county_reports),
    )
    county_areas = map(lambda x: x.area_difference_score, county_reports)
    state_report.median_county_area_difference_score = statistics.median(county_areas)
    state_report.worst_county_area_difference_score = get_worst_area_diff(
        county_reports
    )
    return state_report, county_reports


def verify_topology(state_prec_df, state_report):
    """
    returns (StateReport) instance with the topology fields populated e.g. can_use_gerrychain

    :state_prec_df: (GeoDataFrame)
    :state_report: (StateReport)
    """

    def verify_maup(state_prec_gdf, state_report):
        state_county_df = census_us_county_gdf[
            census_us_county_gdf["STATEFP"] == state_report.fips
        ]
        # match their projections (necessary for maup.assign)
        if not state_prec_gdf.crs:
            state_prec_gdf.crs = "epsg:4326"
        state_prec_gdf = state_prec_gdf.to_crs(state_county_df.crs)
        assert state_prec_gdf.crs == state_county_df.crs
        gdf = fix_buffer(state_prec_gdf)
        try:
            maup.assign(gdf, state_county_df)
            print("MAUP assign was successful")
            return True
        except Exception as error:
            print("Unable to use MAUP assign: \n\n", error)
            return False

    def verify_gerrychain(df):
        try:
            Graph.from_geodataframe(fix_buffer(df))
            print("GerryChain graph created")
            return True
        except Exception as error:
            print("Unable to create GerryChain graph: ", error)
            return False

    prec_geom = state_prec_df.geometry
    valid_rows = state_prec_df[~(prec_geom.isna() | prec_geom.is_empty)]
    if valid_rows.shape[0] != state_prec_df.shape[0]:
        invalid_rows = state_prec_df[prec_geom.isna() | prec_geom.is_empty]
        print("Invalid rows: ", invalid_rows)
        return state_report
    else:
        state_report.all_precincts_have_a_geometry = True
        state_report.can_use_gerrychain = verify_gerrychain(state_prec_df)
        state_report.can_use_maup = verify_maup(state_prec_df, state_report)
        return state_report


def report_lst_to_df(report_lst):
    name_to_cols = defaultdict(list)
    for report in report_lst:
        report_dict = vars(report)
        for key, value in report_dict.items():
            name_to_cols[key].append(value)
    df = pd.DataFrame.from_dict(name_to_cols)
    return df


def make_report(path, state_report, county_report_lst):
    """
    write markdown report to file at `reports/<path>.md'

    :path: (str) filepath to write the output
    :state_report: (StateReport)
    :county_report: ((CountyReport) list)
    """
    github_link = "https://github.com/OpenPrecincts/verification"
    breakdown_link = (
        "https://github.com/OpenPrecincts/verification#verification-report-breakdown"
    )

    state_report = report_lst_to_df([state_report])

    quality_score_columns = [
        "vote_score",
        "county_vote_score_dispersion",
        "worst_county_vote_score",
        "median_county_area_difference_score",
        "worst_county_area_difference_score",
    ]

    quality_score_md = (
        state_report[quality_score_columns]
        .loc[0]
        .rename("")
        .rename(
            {
                "vote_score": "[vote_score](https://github.com/OpenPrecincts/verification#vote-score)",
                "county_vote_score_dispersion": "[county_vote_score_dispersion](https://github.com/OpenPrecincts/verification#county-vote-score-dispersion)",
                "worst_county_vote_score": "[worst_county_vote_score](https://github.com/OpenPrecincts/verification#vote-score)",
                "median_county_area_difference_score": "[median_county_area_difference_score](https://github.com/OpenPrecincts/verification#area-difference-score)",
                "worst_county_area_difference_score": "[worst_county_area_difference_score](https://github.com/OpenPrecincts/verification#area-difference-score)",
            }
        )
        .to_markdown()
    )

    library_compatibility = ["can_use_maup", "can_use_gerrychain"]

    library_compatibility_md = (
        state_report[library_compatibility]
        .loc[0]
        .rename("")
        .to_markdown()
        .replace("1", "✅")
        .replace("0", "❌")
    )

    raw_data_columns = [
        "all_precincts_have_a_geometry",
        "n_votes_democrat_expected",
        "n_votes_republican_expected",
        "n_two_party_votes_expected",
        "n_votes_democrat_observed",
        "n_votes_republican_observed",
        "n_two_party_votes_observed",
    ]

    raw_data = state_report[raw_data_columns].loc[0].rename("")
    raw_data.all_precincts_have_a_geometry = (
        raw_data.all_precincts_have_a_geometry.astype("int")
        .astype("str")
        .replace("1", "✅")
        .replace("0", "❌")
    )
    raw_data_md = raw_data.to_markdown()

    county_reports_df = report_lst_to_df(county_report_lst)
    county_reports = county_reports_df[
        [
            "geoid",
            "name",
            "vote_score",
            "area_difference_score",
            "n_votes_democrat_expected",
            "n_votes_republican_expected",
            "n_two_party_votes_expected",
            "n_votes_democrat_observed",
            "n_votes_republican_observed",
            "n_two_party_votes_observed",
        ]
    ]
    county_reports_md = county_reports.to_markdown(showindex=False)

    report = """
# Election Shapefile Verification Report

[Open Precincts Verification Script]({})

[Verification Report Breakdown]({})

## Validation Metadata
* `Year Validated:` {} 
* `Race Validated:` {}
* `State Validated:` {}
* `File Provider:` {}

## Statewide Reports

### Quality Scores:
{}

### Library Compatibility:
{}

### Raw Data:
{}

## County Level Reports
{}
""".format(
        github_link,
        breakdown_link,
        state_report.year.values[0],
        state_report.office.values[0],
        state_report.abbreviation.values[0],
        state_report.source.values[0],
        quality_score_md,
        library_compatibility_md,
        raw_data_md,
        county_reports_md,
    )

    if "." in path:
        path = path.split(".")[0]
    with open("reports/{}.md".format(path), "w") as text_file:
        text_file.write(report)


def verify_state(
    state_prec_gdf,
    state_abbreviation,
    source,
    year,
    county_level_results_df,
    office,
    d_col=None,
    r_col=None,
    path=None,
):
    """
    returns a complete (StateReport) object and a ((CountyReport) list) for the state.

    :state_prec_gdf: (GeoDataFrame) containing precinct geometries and election results
    :state_abbreviation: (str) e.g. 'MA' for Massachusetts
    :source: (str) person or organization that made the 'state_prec_gdf' e.g 'VEST'
    :year: (str) 'YYYY' indicating the year the election took place e.g. '2016'
    :county_level_results_df: (DataFrame) containing official county-level election results
    :office: (str) office to be evaluated in vote validation e.g. 'U.S. Senate'
    :d_col: (str) denotes the column for democratic vote counts in each precinct
    :r_col: (str) denotes the column for republican vote counts in each precinct
    :path: (str) filepath to which the report should be saved (if None it won't be saved)

    d_col, r_col are optional - if they are not provided, `get_party_cols` will be used
    to guess based on comparing each column in state_prec_gdf to the expected results.
    """
    print("Starting verification process for: ", state_abbreviation, source, year)

    state_prec_gdf = state_prec_gdf.reset_index()
    county_level_results_df = county_level_results_df.reset_index()

    # enforce expected schema
    assert "geometry" in state_prec_gdf.columns
    assert {"county", "GEOID", "party", "votes"}.issubset(
        set(county_level_results_df.columns)
    )

    # assign d_col and r_col
    if not d_col or not r_col:
        print("Candidate vote count columns are being assigned automatically")
        d_col, r_col = get_party_cols(state_prec_gdf, state_abbreviation)
    else:
        print("Candidate vote count columns are being assigned manually")
    print("Choose d_col as: ", d_col)
    print("Choose r_col as: ", r_col)
    state_prec_gdf = state_prec_gdf.rename(columns={d_col: "d_col", r_col: "r_col"})

    # remove unecessary columns
    cols_to_keep = ["d_col", "r_col", "geometry"]
    if "GEOID" in state_prec_gdf.columns:
        cols_to_keep.append("GEOID")
    state_prec_gdf = state_prec_gdf[cols_to_keep]
    print("Verification will now begin with this GeoDataFrame: \n")
    print(state_prec_gdf.head())

    # initialize state report
    print("Starting Vote Verification")
    state_report = StateReport(
        county_level_results_df,
        state_prec_gdf,
        state_abbreviation,
        year,
        source,
        office,
    )

    # poplulate the report
    print("Starting Topology Verification")
    state_report = verify_topology(state_prec_gdf, state_report)

    print("Starting County Verification")
    # assign GEOID
    if "GEOID" not in state_prec_gdf.columns:
        try:
            print("Missing GEOID Column - attempting automatic assignment")
            state_prec_gdf = assign_GEOID(state_prec_gdf, state_report.fips)
            print("GEOID assignment successful")
        except:
            pass
    else:
        print("Using the GEOID Column in the original shapefile.")
    assert "GEOID" in state_prec_gdf.columns

    state_report, county_reports = verify_counties(
        state_prec_gdf, county_level_results_df, state_report
    )
    if path:
        make_report(path, state_report, county_reports)
    print("All done!\n")
    return state_report, county_reports


def verify_state_2016(
    state_prec_gdf, state_abbreviation, source, d_col=None, r_col=None, path=None
):
    """
    returns a complete (StateReport) object and a ((CountyReport) list) for the state.

    :state_prec_gdf: (GeoDataFrame) containing precinct geometries and election results
    :state_abbreviation: (str) e.g. 'MA' for Massachusetts
    :source: (str) person or organization that made the 'state_prec_gdf' e.g 'VEST'
    :d_col: (str) denotes the column for Hillary Clinton vote counts in each precinct
    :r_col: (str) denotes the column for Donald Trump vote counts in each precinct
    :path: (str) filepath to which the report should be saved (if None it won't be saved)

    d_col, r_col are optional - if they are not provided, `get_party_cols` will be used
    to guess based on comparing each column in state_prec_gdf to the expected results.

    Applies 2016 defaults:
    * Uses Official County Results from the 2016 Presidential Election
    * Sets year to '2016'
    * Sets office to 'President'
    """

    results_df = expected_election_results_2016[
        expected_election_results_2016["state_po"] == state_abbreviation
    ]
    return verify_state(
        state_prec_gdf,
        state_abbreviation,
        source,
        2016,
        results_df,
        "President",
        d_col=d_col,
        r_col=r_col,
        path=path,
    )
