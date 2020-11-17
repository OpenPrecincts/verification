import geopandas as gpd
import pandas as pd
import shapely as shp

# Expected Geomerty Shapefiles
census_us_county_gdf = gpd.read_file("./data/county_shapefiles/cb_2016_us_county_500k")
census_us_county_gdf["NAME"] = census_us_county_gdf["NAME"].str.lower()

# Remove alaska because it uses state house districts instead of counties for reporting
census_us_county_gdf = census_us_county_gdf[census_us_county_gdf.STATEFP != "02"]
census_us_county_gdf = census_us_county_gdf[
    ["STATEFP", "COUNTYFP", "GEOID", "NAME", "geometry"]
]

# 15005, Kalawao County has 86 people is combined with 15009,
# Maui County population 167,417 in the eleciton results
# to match the election results, we combine them here under Maui
poly = shp.ops.cascaded_union(
    census_us_county_gdf[census_us_county_gdf.GEOID.isin(["15005", "15009"])][
        "geometry"
    ]
)
census_us_county_gdf.loc[
    (census_us_county_gdf.GEOID == "15009"), "geometry"
] = gpd.GeoSeries(poly)
census_us_county_gdf = census_us_county_gdf.drop(
    census_us_county_gdf[census_us_county_gdf.GEOID == "15005"].index
)


alaska_districts = gpd.read_file("./data/county_shapefiles/2013-HD-ProclamationPlan")
alaska_districts["STATEFP"] = "02"
alaska_districts["COUNTYFP"] = alaska_districts["District_N"].apply(
    lambda x: x.zfill(3)
)
alaska_districts["GEOID"] = alaska_districts["STATEFP"].map(str) + alaska_districts[
    "COUNTYFP"
].map(str)
alaska_districts["NAME"] = alaska_districts["District_N"].apply(
    lambda x: "district " + x
)
alaska_districts = alaska_districts[
    ["STATEFP", "COUNTYFP", "GEOID", "NAME", "geometry"]
]
alaska_districts.to_crs("epsg:4269")

census_us_county_gdf = gpd.GeoDataFrame(
    pd.concat([census_us_county_gdf, alaska_districts]), crs="epsg:4269"
)


# Expected Election Results
county_level_results_df = pd.read_csv("data/election_results/countypres_2000-2016.csv")
county_level_results_df = county_level_results_df[
    county_level_results_df.year == 2016
].reset_index()
county_level_results_df = county_level_results_df[
    ~county_level_results_df.FIPS.isnull()
]
county_level_results_df["county"] = county_level_results_df["county"].str.lower()

# county level results Corrections:

# Kansas city, MO is seperated from the rest of jackson county for some reason
# in the results file it is mistakenly assgined a FIPS code of 36000
# I will combine the KCMO and Jackon County resutls under Jackon County, MO (FIPS = 29095)
county_level_results_df.loc[4500, "candidatevotes"] = (
    county_level_results_df.loc[4500, "candidatevotes"]
    + county_level_results_df.loc[5394, "candidatevotes"]
)
county_level_results_df.loc[4501, "candidatevotes"] = (
    county_level_results_df.loc[4501, "candidatevotes"]
    + county_level_results_df.loc[5395, "candidatevotes"]
)
# remove beford city, va (FIPS = 51515) from results because it was part of bedford county in 2016, and kansas City, MO (FIPS = 36000)
county_level_results_df = county_level_results_df[
    ~(county_level_results_df["FIPS"].isin([36000, 51515]))
]
county_level_results_df = county_level_results_df[
    ~county_level_results_df.FIPS.isnull()
]
county_level_results_df["GEOID"] = county_level_results_df["FIPS"].apply(
    lambda x: str(int(x)).zfill(5)
)

expected_election_results_2016 = county_level_results_df[
    ["state_po", "county", "GEOID", "party", "candidatevotes"]
]
expected_election_results_2016 = expected_election_results_2016.rename(
    columns={"candidatevotes": "votes"}
).reset_index()
