# FlakiMe replication package

This repository contains the necessary scripts to run and extract the results presented in:  _FlakiMe: Laboratory-Controlled Test FlakinessImpact Assessment_

## Structure

Tthis repository is composed of different scripts and archives whose role are described bellow:
- `run-arja*.sh` : These scripts allow to run the probabilistic program repair using [ARJA](https://github.com/yyxhdy/arja). The script annotated by `-all` allows to run the experiment on all the targeted projects with 1 command (recomended).
- `run-pit*.sh` : These scripts allow to run the mutation testing experiment using a [forked version of pitest](https://github.com/UL-SnT-Serval/pitest.git). The script annotated by `-all` allows to run the experiment on all the targeted projects with 1 command (recomended).
- `run-prapr*.sh` : These scripts allow to run the deterministic program repair using [PR-APR](https://github.com/prapr/prapr). The script annotated by `-all` allows to run the experiment on all the targeted projects with 1 command (recomended).
- `run-sbfl*.sh` : TODO
- `*.py` : These scripts allow to plot and analyse the different outputs from the experiments
- `defects4j\` : This folder contains the different project (i.e., `time,math,mock,chart,lang`) in which the a subfolder identified by [defects4j](https://github.com/rjust/defects4j) bug id contains the targeted version.
- `current\` : This folder contains the last stable version of the four targeted projects (`common-lang,common-math,joda-time,jfreechart`).
- `figures\` : This folder contains sample plots build using the most recent results.

## Test subjects
The following table shows the tests subjects for each of the experiments

| Experiment                   | Test subject*                                                                                                                                                                                         |
|------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Mutation testing             |  <ul> <li>Apache-commons-Math : `Latest`</li> <li>Apache-commons-Lang : `Latest`</li> <li>jFreeChart : `Latest` </li> <li>Joda-time : `Latest` </li> </ul>                                           |
| Probabilistic Program repair | <ul>  <li>Apache-commons-Math : `5,34,50,82,85`</li>  <li>Apache-commons-Lang : `6`</li>  <li>Mockito: `29,38` </li>  <li>Joda-time : `11,19` </li> <li>jFreeChart : `1,11,12,20,24,26` </li>  </ul> |
| Deterministic Program repair | <ul>  <li>Apache-commons-Math : `22,39,5,50,53,58,70,98`</li>  <li>Apache-commons-Lang : `20,22,39`</li>  </ul>                                                                                      |
| Fault localization           |   <ul>  <li>Apache-commons-Math : `22,39,5,50,53,58,70,98`</li>  <li>Apache-commons-Lang : `20,22,39`</li>  </ul>                                                                                                                                                                                                   |

\* The test subject are referenced by `name` and `version used`. The `version used` can either be `latest` refering to the last released version or a number which reference the Defects4j `bug-id`
## Usage
### Mutation testing (pitest)
TODO
#### Experiment
TODO
#### Analysis & plot
TODO
### Probabilistic program repair (ARJA)
TODO
#### Experiment
TODO
#### Analysis & plot
TODO
### Deterministic program repair (PR-APR)
TODO
#### Experiment
TODO
#### Analysis & plot
TODO
### Fault localisation (SBFL)
TODO
#### Experiment
TODO
#### Analysis & plot
