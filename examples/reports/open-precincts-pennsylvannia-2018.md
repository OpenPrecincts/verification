
# Election Shapefile Verification Report

[Open Precincts Verification Script](https://github.com/OpenPrecincts/verification)

[Verification Report Breakdown](https://github.com/OpenPrecincts/verification#verification-report-breakdown)

## Validation Metadata
* `Year Validated:` 2018 
* `Race Validated:` U.S. Senate
* `State Validated:` PA
* `File Provider:` Princeton Gerrymandering Project

## Statewide Reports

### Quality Scores:
|                                                                                                            |                |
|:-----------------------------------------------------------------------------------------------------------|---------------:|
| [vote_score](https://github.com/OpenPrecincts/verification#vote-score)                                     |    1.00007     |
| [county_vote_score_dispersion](https://github.com/OpenPrecincts/verification#county-vote-score-dispersion) | 6322.24        |
| [worst_county_vote_score](https://github.com/OpenPrecincts/verification#vote-score)                        |    1.04645     |
| [median_county_area_difference_score](https://github.com/OpenPrecincts/verification#area-difference-score) |    0.000713403 |
| [worst_county_area_difference_score](https://github.com/OpenPrecincts/verification#area-difference-score)  |    0.00765105  |

### Library Compatibility:
|                    |    |
|:-------------------|---:|
| can_use_maup       |  ✅ |
| can_use_gerrychain |  ✅ |

### Raw Data:
|                               |         |
|:------------------------------|:--------|
| all_precincts_have_a_geometry | ✅      |
| n_votes_democrat_expected     | 2792437 |
| n_votes_republican_expected   | 2134848 |
| n_two_party_votes_expected    | 4927285 |
| n_votes_democrat_observed     | 2792656 |
| n_votes_republican_observed   | 2134991 |
| n_two_party_votes_observed    | 4927647 |

## County Level Reports
|   geoid | name                  |   vote_score |   area_difference_score |   n_votes_democrat_expected |   n_votes_republican_expected |   n_two_party_votes_expected |   n_votes_democrat_observed |   n_votes_republican_observed |   n_two_party_votes_observed |
|--------:|:----------------------|-------------:|------------------------:|----------------------------:|------------------------------:|-----------------------------:|----------------------------:|------------------------------:|-----------------------------:|
|   42001 | Adams County          |     1        |             0.000762873 |                       14880 |                         23419 |                        38299 |                       14880 |                         23419 |                        38299 |
|   42003 | Allegheny County      |     1        |             0.000491828 |                      355907 |                        176351 |                       532258 |                      355907 |                        176351 |                       532258 |
|   42005 | Armstrong County      |     1        |             0.000826309 |                        8570 |                         15449 |                        24019 |                        8570 |                         15449 |                        24019 |
|   42007 | Beaver County         |     1        |             0.000504956 |                       34442 |                         31916 |                        66358 |                       34442 |                         31916 |                        66358 |
|   42009 | Bedford County        |     1        |             0.000440888 |                        4567 |                         14044 |                        18611 |                        4567 |                         14044 |                        18611 |
|   42011 | Berks County          |     0.999993 |             0.000442192 |                       73714 |                         68159 |                       141873 |                       73713 |                         68159 |                       141872 |
|   42013 | Blair County          |     1.00012  |             0.00116668  |                       14599 |                         27826 |                        42425 |                       14602 |                         27828 |                        42430 |
|   42015 | Bradford County       |     0.995641 |             0.000448954 |                        6926 |                         13032 |                        19958 |                        6900 |                         12971 |                        19871 |
|   42017 | Bucks County          |     1        |             0.00157264  |                      165408 |                        124133 |                       289541 |                      165408 |                        124133 |                       289541 |
|   42019 | Butler County         |     1        |             0.00147183  |                       31010 |                         46875 |                        77885 |                       31010 |                         46875 |                        77885 |
|   42021 | Cambria County        |     1        |             0.00112042  |                       21590 |                         27367 |                        48957 |                       21590 |                         27367 |                        48957 |
|   42023 | Cameron County        |     1        |             0.00153223  |                         653 |                          1080 |                         1733 |                         653 |                          1080 |                         1733 |
|   42025 | Carbon County         |     1        |             0.000624512 |                        8739 |                         13519 |                        22258 |                        8739 |                         13519 |                        22258 |
|   42027 | Centre County         |     1        |             0.00060579  |                       34778 |                         24332 |                        59110 |                       34778 |                         24332 |                        59110 |
|   42029 | Chester County        |     1        |             0.00128803  |                      140138 |                         92380 |                       232518 |                      140138 |                         92380 |                       232518 |
|   42031 | Clarion County        |     1        |             0.000877755 |                        4924 |                          8838 |                        13762 |                        4924 |                          8838 |                        13762 |
|   42033 | Clearfield County     |     1        |             0.000652196 |                        9540 |                         16852 |                        26392 |                        9540 |                         16852 |                        26392 |
|   42035 | Clinton County        |     1        |             0.000692122 |                        5289 |                          6869 |                        12158 |                        5289 |                          6869 |                        12158 |
|   42037 | Columbia County       |     1        |             0.000652698 |                        8837 |                         13437 |                        22274 |                        8837 |                         13437 |                        22274 |
|   42039 | Crawford County       |     1        |             0.000342731 |                       11720 |                         17813 |                        29533 |                       11720 |                         17813 |                        29533 |
|   42041 | Cumberland County     |     1        |             0.00160245  |                       47738 |                         54525 |                       102263 |                       47738 |                         54525 |                       102263 |
|   42043 | Dauphin County        |     1        |             0.00414084  |                       59533 |                         47152 |                       106685 |                       59533 |                         47152 |                       106685 |
|   42045 | Delaware County       |     1        |             0.00260445  |                      163216 |                         84423 |                       247639 |                      163216 |                         84423 |                       247639 |
|   42047 | Elk County            |     1        |             0.00174254  |                        4498 |                          6610 |                        11108 |                        4498 |                          6610 |                        11108 |
|   42049 | Erie County           |     1        |             0.00765105  |                       58906 |                         40348 |                        99254 |                       58906 |                         40348 |                        99254 |
|   42051 | Fayette County        |     1        |             0.0009279   |                       19563 |                         20514 |                        40077 |                       19563 |                         20514 |                        40077 |
|   42053 | Forest County         |     0.999472 |             0.00124501  |                         693 |                          1201 |                         1894 |                         692 |                          1201 |                         1893 |
|   42055 | Franklin County       |     1        |             0.000702464 |                       17385 |                         36735 |                        54120 |                       17385 |                         36735 |                        54120 |
|   42057 | Fulton County         |     1        |             0.0006684   |                        1061 |                          4173 |                         5234 |                        1061 |                          4173 |                         5234 |
|   42059 | Greene County         |     1        |             0.00106898  |                        5819 |                          6422 |                        12241 |                        5819 |                          6422 |                        12241 |
|   42061 | Huntingdon County     |     1        |             0.000431619 |                        5126 |                         10491 |                        15617 |                        5126 |                         10491 |                        15617 |
|   42063 | Indiana County        |     1        |             0.000590801 |                       12702 |                         16314 |                        29016 |                       12702 |                         16314 |                        29016 |
|   42065 | Jefferson County      |     1        |             0.000491797 |                        4437 |                         10872 |                        15309 |                        4437 |                         10872 |                        15309 |
|   42067 | Juniata County        |     0.998548 |             0.000918149 |                        2412 |                          5853 |                         8265 |                        2409 |                          5844 |                         8253 |
|   42069 | Lackawanna County     |     1        |             0.000825345 |                       51444 |                         31922 |                        83366 |                       51444 |                         31922 |                        83366 |
|   42071 | Lancaster County      |     1        |             0.000672803 |                       90521 |                        107454 |                       197975 |                       90521 |                        107454 |                       197975 |
|   42073 | Lawrence County       |     1        |             0.00327414  |                       14324 |                         17375 |                        31699 |                       14324 |                         17375 |                        31699 |
|   42075 | Lebanon County        |     1        |             0.000360864 |                       18368 |                         29836 |                        48204 |                       18368 |                         29836 |                        48204 |
|   42077 | Lehigh County         |     1        |             0.000716573 |                       73632 |                         52576 |                       126208 |                       73632 |                         52576 |                       126208 |
|   42079 | Luzerne County        |     1        |             0.00038713  |                       49200 |                         58040 |                       107240 |                       49200 |                         58040 |                       107240 |
|   42081 | Lycoming County       |     1        |             0.000505788 |                       13893 |                         26488 |                        40381 |                       13893 |                         26488 |                        40381 |
|   42083 | McKean County         |     1        |             0.00045121  |                        3972 |                          8285 |                        12257 |                        3972 |                          8285 |                        12257 |
|   42085 | Mercer County         |     1        |             0.000436643 |                       18136 |                         22290 |                        40426 |                       18136 |                         22290 |                        40426 |
|   42087 | Mifflin County        |     1.04645  |             0.000474396 |                        3934 |                          9564 |                        13498 |                        4188 |                          9937 |                        14125 |
|   42089 | Monroe County         |     1        |             0.000967372 |                       30626 |                         23968 |                        54594 |                       30626 |                         23968 |                        54594 |
|   42091 | Montgomery County     |     0.9996   |             0.000599364 |                      248454 |                        126666 |                       375120 |                      248454 |                        126516 |                       374970 |
|   42093 | Montour County        |     0.999276 |             0.00163489  |                        2966 |                          3943 |                         6909 |                        2963 |                          3941 |                         6904 |
|   42095 | Northampton County    |     1        |             0.00153782  |                       62275 |                         50385 |                       112660 |                       62275 |                         50385 |                       112660 |
|   42097 | Northumberland County |     0.999508 |             0.00116656  |                       10524 |                         17926 |                        28450 |                       10521 |                         17915 |                        28436 |
|   42099 | Perry County          |     1        |             0.000840822 |                        5186 |                         11607 |                        16793 |                        5186 |                         11607 |                        16793 |
|   42101 | Philadelphia County   |     1        |             0.00666779  |                      481467 |                         66653 |                       548120 |                      481467 |                         66653 |                       548120 |
|   42103 | Pike County           |     1        |             0.00108902  |                        8696 |                         11772 |                        20468 |                        8696 |                         11772 |                        20468 |
|   42105 | Potter County         |     1        |             0.00040153  |                        1537 |                          4564 |                         6101 |                        1537 |                          4564 |                         6101 |
|   42107 | Schuylkill County     |     1        |             0.000496391 |                       17691 |                         30452 |                        48143 |                       17691 |                         30452 |                        48143 |
|   42109 | Snyder County         |     1        |             0.00082335  |                        4322 |                          8826 |                        13148 |                        4322 |                          8826 |                        13148 |
|   42111 | Somerset County       |     1        |             0.000713403 |                        9322 |                         18896 |                        28218 |                        9322 |                         18896 |                        28218 |
|   42113 | Sullivan County       |     1        |             0.000723782 |                         962 |                          1720 |                         2682 |                         962 |                          1720 |                         2682 |
|   42115 | Susquehanna County    |     1        |             0.00050088  |                        5521 |                         10112 |                        15633 |                        5520 |                         10113 |                        15633 |
|   42117 | Tioga County          |     1        |             0.000517018 |                        4145 |                         10242 |                        14387 |                        4145 |                         10242 |                        14387 |
|   42119 | Union County          |     1        |             0.000812342 |                        5901 |                          8317 |                        14218 |                        5901 |                          8317 |                        14218 |
|   42121 | Venango County        |     1        |             0.000460417 |                        6945 |                         11210 |                        18155 |                        6945 |                         11210 |                        18155 |
|   42123 | Warren County         |     1        |             0.000697455 |                        5390 |                          8734 |                        14124 |                        5390 |                          8734 |                        14124 |
|   42125 | Washington County     |     1        |             0.000633807 |                       39220 |                         41958 |                        81178 |                       39220 |                         41958 |                        81178 |
|   42127 | Wayne County          |     1        |             0.000872762 |                        7625 |                         12269 |                        19894 |                        7625 |                         12269 |                        19894 |
|   42129 | Westmoreland County   |     1        |             0.000819782 |                       63778 |                         79078 |                       142856 |                       63778 |                         79078 |                       142856 |
|   42131 | Wyoming County        |     1        |             0.000645428 |                        3868 |                          6582 |                        10450 |                        3868 |                          6582 |                        10450 |
|   42133 | York County           |     1        |             0.000666381 |                       69272 |                         95814 |                       165086 |                       69272 |                         95814 |                       165086 |
