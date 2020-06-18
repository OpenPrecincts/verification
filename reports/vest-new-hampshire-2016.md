
# Election Shapefile Verification Report

[Open Precincts Verification Script](https://github.com/OpenPrecincts/verification)

[Verification Report Breakdown](https://github.com/OpenPrecincts/verification#verification-report-fields)
## Statewide Reports

### Quality Scores:
|                                                                                                            |            |
|:-----------------------------------------------------------------------------------------------------------|-----------:|
| [vote_score](https://github.com/OpenPrecincts/verification#vote-score)                                     | 1          |
| [county_vote_score_dispersion](https://github.com/OpenPrecincts/verification#county-vote-score-dispersion) | 0          |
| [worst_county_vote_score](https://github.com/OpenPrecincts/verification#vote-score)                        | 1          |
| [median_county_area_difference_score](https://github.com/OpenPrecincts/verification#area-difference-score) | 0.00107231 |
| [worst_county_area_difference_score](https://github.com/OpenPrecincts/verification#area-difference-score)  | 0.0869853  |

### Library Compatibility:
|                    |    |
|:-------------------|---:|
| can_use_maup       |  ✅ |
| can_use_gerrychain |  ✅ |

### Raw Data:
|                               |          |
|:------------------------------|:---------|
| all_precincts_have_a_geometry | ✅       |
| n_votes_democrat_expected     | 348526.0 |
| n_votes_republican_expected   | 345790.0 |
| n_two_party_votes_expected    | 694316.0 |
| n_votes_democrat_observed     | 348526   |
| n_votes_republican_observed   | 345790   |
| n_two_party_votes_observed    | 694316   |

## County Level Reports
|   geoid | name                |   vote_score |   area_difference_score |   n_votes_democrat_expected |   n_votes_republican_expected |   n_two_party_votes_expected |   n_votes_democrat_observed |   n_votes_republican_observed |   n_two_party_votes_observed |
|--------:|:--------------------|-------------:|------------------------:|----------------------------:|------------------------------:|-----------------------------:|----------------------------:|------------------------------:|-----------------------------:|
|   33001 | Belknap County      |            1 |             0.00105878  |                       13517 |                         19315 |                        32832 |                       13517 |                         19315 |                        32832 |
|   33003 | Carroll County      |            1 |             0.000835692 |                       12987 |                         14635 |                        27622 |                       12987 |                         14635 |                        27622 |
|   33005 | Cheshire County     |            1 |             0.00108585  |                       22064 |                         16876 |                        38940 |                       22064 |                         16876 |                        38940 |
|   33007 | Coos County         |            1 |             0.00199538  |                        6563 |                          7952 |                        14515 |                        6563 |                          7952 |                        14515 |
|   33009 | Grafton County      |            1 |             0.000988192 |                       28510 |                         19010 |                        47520 |                       28510 |                         19010 |                        47520 |
|   33011 | Hillsborough County |            1 |             0.000521307 |                       99589 |                        100013 |                       199602 |                       99589 |                        100013 |                       199602 |
|   33013 | Merrimack County    |            1 |             0.000487777 |                       40198 |                         37674 |                        77872 |                       40198 |                         37674 |                        77872 |
|   33015 | Rockingham County   |            1 |             0.0869853   |                       79994 |                         90447 |                       170441 |                       79994 |                         90447 |                       170441 |
|   33017 | Strafford County    |            1 |             0.00270899  |                       34894 |                         29072 |                        63966 |                       34894 |                         29072 |                        63966 |
|   33019 | Sullivan County     |            1 |             0.00146217  |                       10210 |                         10796 |                        21006 |                       10210 |                         10796 |                        21006 |
