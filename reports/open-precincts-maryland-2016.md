
# Election Shapefile Verification Report

[Open Precincts Verification Script](https://github.com/OpenPrecincts/verification)

[Verification Report Breakdown](https://github.com/OpenPrecincts/verification#verification-report-fields)
## Statewide Reports

### Quality Scores:
|                                                                                                            |           |
|:-----------------------------------------------------------------------------------------------------------|----------:|
| [vote_score](https://github.com/OpenPrecincts/verification#vote-score)                                     | 1         |
| [county_vote_score_dispersion](https://github.com/OpenPrecincts/verification#county-vote-score-dispersion) | 0         |
| [vote_score](https://github.com/OpenPrecincts/verification#vote-score)                                     | 1         |
| [median_county_area_difference_score](https://github.com/OpenPrecincts/verification#area-difference-score) | 0.0300684 |
| [worst_county_area_difference_score](https://github.com/OpenPrecincts/verification#area-difference-score)  | 0.229951  |

### Library Compatibility:
|                    |    |
|:-------------------|---:|
| can_use_maup       |  ✅ |
| can_use_gerrychain |  ✅ |

### Raw Data:
|                               |           |
|:------------------------------|:----------|
| all_precincts_have_a_geometry | ✅        |
| n_votes_democrat_expected     | 1677928.0 |
| n_votes_republican_expected   | 943169.0  |
| n_two_party_votes_expected    | 2621097.0 |
| n_votes_democrat_observed     | 1677928   |
| n_votes_republican_observed   | 943169    |
| n_two_party_votes_observed    | 2621097   |

## County Level Reports
|   geoid | name                   |   vote_score |   area_difference_score |   n_votes_democrat_expected |   n_votes_republican_expected |   n_two_party_votes_expected |   n_votes_democrat_observed |   n_votes_republican_observed |   n_two_party_votes_observed |
|--------:|:-----------------------|-------------:|------------------------:|----------------------------:|------------------------------:|-----------------------------:|----------------------------:|------------------------------:|-----------------------------:|
|   24001 | Allegany County        |            1 |              0.00312633 |                        7875 |                         21270 |                        29145 |                        7875 |                         21270 |                        29145 |
|   24003 | Anne Arundel County    |            1 |              0.0852648  |                      128419 |                        122403 |                       250822 |                      128419 |                        122403 |                       250822 |
|   24510 | Baltimore city         |            1 |              0.0624491  |                      202673 |                         25205 |                       227878 |                      202673 |                         25205 |                       227878 |
|   24005 | Baltimore County       |            1 |              0.0259037  |                      218412 |                        149477 |                       367889 |                      218412 |                        149477 |                       367889 |
|   24009 | Calvert County         |            1 |              0.11044    |                       18225 |                         26176 |                        44401 |                       18225 |                         26176 |                        44401 |
|   24011 | Caroline County        |            1 |              0.00157089 |                        4009 |                          9368 |                        13377 |                        4009 |                          9368 |                        13377 |
|   24013 | Carroll County         |            1 |              0.00377215 |                       26567 |                         58215 |                        84782 |                       26567 |                         58215 |                        84782 |
|   24015 | Cecil County           |            1 |              0.0792286  |                       13650 |                         28868 |                        42518 |                       13650 |                         28868 |                        42518 |
|   24017 | Charles County         |            1 |              0.0537216  |                       49341 |                         25614 |                        74955 |                       49341 |                         25614 |                        74955 |
|   24019 | Dorchester County      |            1 |              0.0488164  |                        6245 |                          8413 |                        14658 |                        6245 |                          8413 |                        14658 |
|   24021 | Frederick County       |            1 |              0.0024901  |                       56522 |                         59522 |                       116044 |                       56522 |                         59522 |                       116044 |
|   24023 | Garrett County         |            1 |              0.00147298 |                        2567 |                         10776 |                        13343 |                        2567 |                         10776 |                        13343 |
|   24025 | Harford County         |            1 |              0.030471   |                       47077 |                         77860 |                       124937 |                       47077 |                         77860 |                       124937 |
|   24027 | Howard County          |            1 |              0.00187875 |                      102597 |                         47484 |                       150081 |                      102597 |                         47484 |                       150081 |
|   24029 | Kent County            |            1 |              0.0120449  |                        4575 |                          4876 |                         9451 |                        4575 |                          4876 |                         9451 |
|   24031 | Montgomery County      |            1 |              0.00268043 |                      357837 |                         92704 |                       450541 |                      357837 |                         92704 |                       450541 |
|   24033 | Prince George's County |            1 |              0.0296659  |                      344049 |                         32811 |                       376860 |                      344049 |                         32811 |                       376860 |
|   24035 | Queen Anne's County    |            1 |              0.0346297  |                        7973 |                         16993 |                        24966 |                        7973 |                         16993 |                        24966 |
|   24039 | Somerset County        |            1 |              0.0702953  |                        4196 |                          5341 |                         9537 |                        4196 |                          5341 |                         9537 |
|   24037 | St. Mary's County      |            1 |              0.107291   |                       17534 |                         28663 |                        46197 |                       17534 |                         28663 |                        46197 |
|   24041 | Talbot County          |            1 |              0.115895   |                        8653 |                         10724 |                        19377 |                        8653 |                         10724 |                        19377 |
|   24043 | Washington County      |            1 |              0.00288996 |                       21129 |                         40998 |                        62127 |                       21129 |                         40998 |                        62127 |
|   24045 | Wicomico County        |            1 |              0.00740395 |                       18050 |                         22198 |                        40248 |                       18050 |                         22198 |                        40248 |
|   24047 | Worcester County       |            1 |              0.229951   |                        9753 |                         17210 |                        26963 |                        9753 |                         17210 |                        26963 |
