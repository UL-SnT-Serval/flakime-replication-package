# Test subjects

The following sections describe the tests subjects for each of the experiments. The pom.xml of each of the project was modified to add profiles that allow the use of the different maven plugins namely FlakiMe, PIT and PRAPR. Note that prior to run the scripts contained in `\run`, the projects need to be decompressed.

## Releases

The test subject are referenced by `name` and `version used`. The `version used` refers to the version number used. The projects are placed under the directory `\projects\releases`.

| Experiment                   | Test subject                                                                                                                                                                                      |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Mutation testing             | <ul> <li>Apache-commons-Math : `3.6.1`</li> <li>Apache-commons-Lang : `3.12.0`</li> <li>jFreeChart : `2.0.0` </li> <li>Joda-time : `2.10.10` </li> </ul>                                            |

## Defects4J

The test subject are referenced by `name` and `version used`. The `version used` refers to the Defects4J `bug-id`. The projects are placed under the directory `\projects\defects4j`.

| Experiment                   | Test subject                                                                                                                                                                                        |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Probabilistic Program repair | <ul>  <li>Apache-commons-Math : `5,34,50,82,85`</li>  <li>Apache-commons-Lang : `6`</li>  <li>Mockito: `29,38` </li>  <li>Joda-time : `11,19` </li> <li>jFreeChart : `1,11,12,20,24,26` </li>  </ul> |
| Deterministic Program repair | <ul>  <li>Apache-commons-Math : `22,39,5,50,53,58,70,98`</li>  <li>Apache-commons-Lang : `20,22,39`</li>  </ul>                                                                                      |
| Fault localization           | <ul>  <li>Apache-commons-Math : `22,39,5,50,53,58,70,98`</li>  <li>Apache-commons-Lang : `20,22,39`</li>  </ul>                                                                                      |
