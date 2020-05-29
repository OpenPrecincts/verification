# Verification of Election Shapefiles

Only for 2016 Elections at the moment - 2018 support coming soon!

**Input:** Statewide Precinct Shapefile with election results. Each row should represent a precinct which has a geometry, democratic candidate votes and republican candidate votes.

**Output:** Report comparing the **Input's** election results and geometries with the expected election results and geometries in addition to checking the **Input** for compatibility with MAUP and Gerrychain.

### Sources
* Expected election results are sourced from [MIT Election Data + Science Lab (MEDSL)](https://electionlab.mit.edu/data)
* Expected geometries are sourced from [The United States Census Bureau](https://www.census.gov/) and the [Alaska Division of Elections](http://www.elections.alaska.gov/doc/info/2013-HD-ProclamationPlan.zip)

This verification script generates a report based on comparing the **Input's** election results and geometries with the sources above.

This script compares precinct level election results from the **Input** with the expected election results from official state election data records at the state and county level. In both cases the precinct level results are aggregated up to their state and county respectively and then compared to the expected results. Likewise, the precinct geometries are aggregated up to the county level and compared with the county shapefiles from the US Census Bureau.

In order to do the comparisons detailed above, the script needs to know about the makeup of the **Input** file. Specifically, it needs to know the county (or equivalent) for each precinct and which columns correspond with the votes for Hillary Clinton and Donald Trump for each precinct.

### GEOID/ County assignment for each precinct
The precincts need to be assigned a county in the form of the county's 5 digit GEOID code described below:

#### GEOID SPEC:
Elements of the GEOID column are 5 character strings. The first 2 characters
are the StateFP code and the last 3 characters are the CountyFP code. e.g. 

* Massachusetts' StateFP = '25'
* Essex County's CountyFP = '009'
* Essex County, Massachusetts' GEODID = '25009'

If either code has fewer digits than are allocated, the string representation should
be zero-padded from the left. e.g. Alaska (StateFP = 2) should be '02'.

The GEOID may be given for each precinct in **Input** file. In this case, the column must conform to the spec above and be named `'GEOID'`.
If the GEOID column is missing then the script will attempt to create it using the [MAUP package](https://github.com/mggg/maup#assigning-precincts-to-districts) to assign each precinct to the county which contains it. Omission of the GEOID label in the input file and failure to assign counties with MAUP (e.g. script throws an exception) will result in the report skipping county level metrics (denoted with -1 metric values).

### Candidate vote counts
The script needs to know which column contains votes for Clinton and which column contains votes for Trump. They can be manually entered as arguments:

* `d_col` denotes the column for Hillary Clinton vote counts in each precinct
* `r_col` denotes the column for Donald Trump vote counts in each precinct.

Without those arguments, the script will guess based on the expected number of votes for each candidate.

# Verification Report Fields

## Quality Scores:

### Vote Score

Compute the ratio of votes observed in the **Input** to the votes expected (based on official state election data records from MEDSL) for the democratic and republican candidate. Then the Vote Score is the weighted average of these ratios. [Python Implementation](74)

* Ideally Vote Score = 1
* A Vote Score above 1 indicates that the **Input** contains more recorded votes than the official state election data
* A Vote Score below 1 indicates that the **Input** contains fewer recorded votes than the official state election data.

### County Vote Score Dispersion

For each county, compute the square of the difference between the expected number of votes for the democratic and republican candidate. Then, County Vote Score Dispersion is the average of the square difference across all the counties in the state. [Python Implementation](439)

* Ideally County Vote Score Dispersion = 0
* As the County Vote Score Dispersion increases, so does the degree to which the **Input** differs with respect to official state election data records about the county-level results. 


### Area Difference Score

Compute the symmetric difference between the **Input's** geometries and the expected geometries for that state from the Census Bureau. Then Area Difference Score is the ratio of the symmetric difference's area to the area of the precinct shapefiles. [Python Implementation](176)

* Ideally Area Difference Score is 0
* As the Area Difference Score increases it indicates a greater geometric difference between the observed geometry in the **Input** and the expected geometry.
* An Area Difference Score of -1 indicates an error was encountered when attempting to compute the metric. Therefore, it is the worst value possible for the Area Difference score. 

## Library Compatibility 

Check the **Input** for compatibility with libraries and packages that we hope our end users will be able to apply to the map.

* can_use_maup: `(boolean)` Can use [MAUP](https://github.com/mggg/maup), a geospatial toolkit for redistricting data.
* can_use_gerrychain: `(boolean)` Can use [Gerrychain](https://github.com/mggg/GerryChain) which is useful for applying sensitivity testing via Markov chain Monte Carlo sampling.

## Raw Data

* n_votes_democrat_expected: `(int)` number of votes for the democratic candidate in MEDSL dataset
* n_votes_republican_expected: `(int)` number of votes for the republican candidate in MEDSL dataset
* n_two_party_votes_expected: `(int)` n_votes_republican_expected + n_votes_republican_expected
* n_votes_democrat_observed: `(int)`  number of votes for the democratic candidate in the **Input**
* n_votes_republican_observed: `(int)`  number of votes for the republican candidate in the **Input**
* n_two_party_votes_observed: `(int)`  n_votes_democrat_observed + n_votes_republican_observed
* all_precincts_have_a_geometry: `(int)`  every precinct has a valid geometry
