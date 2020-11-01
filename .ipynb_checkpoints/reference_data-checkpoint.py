import pandas as pd
import warnings
from collections import defaultdict
warnings.simplefilter(action='ignore', category=FutureWarning)


# Lookup tables
state_to_state_po = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "District of Columbia": "DC",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
}

state_abbreviation_to_state_name = dict(map(reversed, state_to_state_po.items()))

kdf = pd.read_csv("data/fips_data/fips.csv")
state_to_fips = pd.Series(kdf.fips.values, index=kdf.name).to_dict()
fips_to_state = dict(map(reversed, state_to_fips.items()))

df = pd.read_csv("data/fips_data/countyFip.csv")
# remove PR
df = df[df.state_fip < 72]
df["GEOID"] = df.state_fip.apply(lambda x: str(x).zfill(2)) + df.county_fip.apply(
    lambda x: str(x).zfill(3)
)

state_fip_to_geoids_seen = defaultdict(set)
indices_to_drop = set()
for index, row in df.iterrows():
    if row['GEOID'] in state_fip_to_geoids_seen[row['state_fip']]:
        indices_to_drop.add(index)
    else:
        state_fip_to_geoids_seen[row['state_fip']].add(row['GEOID'])
df = df.drop(indices_to_drop)
df['state'] = df['state_fip'].map(fips_to_state)
df['state_po'] = df['state'].map(state_to_state_po)


geoid_to_county_name = pd.Series(df["county_name"].values, index=df["GEOID"]).to_dict()
state_fip_to_county_to_geoid = {}
for state_fip in df.state_fip.unique():
    state_df = df[df.state_fip == state_fip]
    state_dict = pd.Series(
        state_df["GEOID"].values, index=state_df["county_name"]
    ).to_dict()
    state_fip_to_county_to_geoid[state_fip] = state_dict



