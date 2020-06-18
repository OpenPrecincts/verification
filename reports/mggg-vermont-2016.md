
# Election Shapefile Verification Report

[Open Precincts Verification Script](https://github.com/OpenPrecincts/verification)

[Verification Report Breakdown](https://github.com/OpenPrecincts/verification#verification-report-fields)
## Statewide Reports

### Quality Scores:
|                                                                                                            |           |
|:-----------------------------------------------------------------------------------------------------------|----------:|
| [vote_score](https://github.com/OpenPrecincts/verification#vote-score)                                     | 1         |
| [county_vote_score_dispersion](https://github.com/OpenPrecincts/verification#county-vote-score-dispersion) | 0         |
| [worst_county_vote_score](https://github.com/OpenPrecincts/verification#vote-score)                        | 1         |
| [median_county_area_difference_score](https://github.com/OpenPrecincts/verification#area-difference-score) | 0.0011365 |
| [worst_county_area_difference_score](https://github.com/OpenPrecincts/verification#area-difference-score)  | 0.322525  |

### Library Compatibility:
|                    |    |
|:-------------------|---:|
| can_use_maup       |  ✅ |
| can_use_gerrychain |  ✅ |

### Raw Data:
|                               |          |
|:------------------------------|:---------|
| all_precincts_have_a_geometry | ✅       |
| n_votes_democrat_expected     | 178573.0 |
| n_votes_republican_expected   | 95369.0  |
| n_two_party_votes_expected    | 273942.0 |
| n_votes_democrat_observed     | 178573   |
| n_votes_republican_observed   | 95369    |
| n_two_party_votes_observed    | 273942   |

## County Level Reports
|   geoid | name              |   vote_score |   area_difference_score |   n_votes_democrat_expected |   n_votes_republican_expected |   n_two_party_votes_expected |   n_votes_democrat_observed |   n_votes_republican_observed |   n_two_party_votes_observed |
|--------:|:------------------|-------------:|------------------------:|----------------------------:|------------------------------:|-----------------------------:|----------------------------:|------------------------------:|-----------------------------:|
|   50005 | Caledonia County  |            1 |             0.00135788  |                        6445 |                          5534 |                        11979 |                        6445 |                          5534 |                        11979 |
|   50001 | Addison County    |            1 |             0.000915124 |                       11219 |                          5297 |                        16516 |                       11219 |                          5297 |                        16516 |
|   50009 | Essex County      |            1 |             0.322525    |                        1019 |                          1506 |                         2525 |                        1019 |                          1506 |                         2525 |
|   50011 | Franklin County   |            1 |             0.000518428 |                        9351 |                          8752 |                        18103 |                        9351 |                          8752 |                        18103 |
|   50015 | Lamoille County   |            1 |             0.000738848 |                        7241 |                          3570 |                        10811 |                        7241 |                          3570 |                        10811 |
|   50021 | Rutland County    |            1 |             0.000841367 |                       13635 |                         12479 |                        26114 |                       13635 |                         12479 |                        26114 |
|   50027 | Windsor County    |            1 |             0.000791351 |                       17556 |                          8605 |                        26161 |                       17556 |                          8605 |                        26161 |
|   50025 | Windham County    |            1 |             0.0376398   |                       14340 |                          5454 |                        19794 |                       14340 |                          5454 |                        19794 |
|   50013 | Grand Isle County |            1 |             0.00182573  |                        2094 |                          1487 |                         3581 |                        2094 |                          1487 |                         3581 |
|   50023 | Washington County |            1 |             0.000878697 |                       18594 |                          7993 |                        26587 |                       18594 |                          7993 |                        26587 |
|   50007 | Chittenden County |            1 |             0.00850849  |                       54814 |                         18601 |                        73415 |                       54814 |                         18601 |                        73415 |
|   50017 | Orange County     |            1 |             0.00171775  |                        7541 |                          5007 |                        12548 |                        7541 |                          5007 |                        12548 |
|   50019 | Orleans County    |            1 |             0.000741648 |                        5185 |                          5159 |                        10344 |                        5185 |                          5159 |                        10344 |
|   50003 | Bennington County |            1 |             0.0707742   |                        9539 |                          5925 |                        15464 |                        9539 |                          5925 |                        15464 |
