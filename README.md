# FlakiMe replication package

This repository contains the necessary scripts to run and extract the results presented in:  _FlakiMe: Laboratory-Controlled Test FlakinessImpact Assessment_

## Structure

This repository is composed of different scripts and archives whose role are described bellow:
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

| Experiment                   | Test subject*                                                                                                                                                                                        |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Mutation testing             | <ul> <li>Apache-commons-Math : `Latest`</li> <li>Apache-commons-Lang : `Latest`</li> <li>jFreeChart : `Latest` </li> <li>Joda-time : `Latest` </li> </ul>                                            |
| Probabilistic Program repair | <ul>  <li>Apache-commons-Math : `5,34,50,82,85`</li>  <li>Apache-commons-Lang : `6`</li>  <li>Mockito: `29,38` </li>  <li>Joda-time : `11,19` </li> <li>jFreeChart : `1,11,12,20,24,26` </li>  </ul> |
| Deterministic Program repair | <ul>  <li>Apache-commons-Math : `22,39,5,50,53,58,70,98`</li>  <li>Apache-commons-Lang : `20,22,39`</li>  </ul>                                                                                      |
| Fault localization           | <ul>  <li>Apache-commons-Math : `22,39,5,50,53,58,70,98`</li>  <li>Apache-commons-Lang : `20,22,39`</li>  </ul>                                                                                      |

\* The test subject are referenced by `name` and `version used`. The `version used` can either be `latest` refering to the last released version or a number which reference the Defects4j `bug-id`
## Usage
**Requirements** :
*Experiment*
- Java version : `8 Update 2xx` with `JAVA_HOME` environment variable set (e.g., `$: export JAVA_HOME=/usr/jdk/jdk1.8.0_271`)
- Apache Maven version : `3.6.3`
- **Extract the project archives** contained in `defects4j\` and `current\`. (*approx*. 1,5 GB total)

*Analysis*
- Python version `3.8.8`
- `Pandas` library
- `Numpy`  library
- `yaml` library
- `matplotlib` library
- `seaborn` library

### Mutation testing (Pitest)
This experiment helps to investigate the effect of flakiness on the mutation score by injecting flaky failure with different nominal flake rate.
#### Experiment
The experiment is describe bellow :

```
0: Foreach Project p in [math,time,chart,lang]:
1:      For nfr from 0 to 0,5:
2:          For 10 repetitions:
3:              Inject_flakiness(p,nfr)
4:              run_Pitest()
5:              record_mutation_score
```
The script `run-pit.sh` corresponds to the last loop(line 2 to 5) and takes as arguments : `$ ./run-pit.sh {project_location} {nominal_flakeRate}`. The script `run-pit-all.sh` corresponds to the first two loops and does not takes arguments.

Thus for running the full experiment (*approx*. 25 hours) use `run-pit-all.sh`. 

Each repetition writes to a file located in `$PROJECT_FOLDER/output_$nfr.out` the following information `ith_rep | #mutant_generated | #flaky_failure | #mutant_killed`

#### Analysis & plot
The plot of results are done using `pit_plot.py` script. The script reads its config (path of output file for each projects, repetition for each nominal flake rates and initial mutation score) from the `config_.yml` file.

To plot the results simply run `python pit_plot.py`. The figures can be found in `figures\`
### Probabilistic program repair (ARJA)
This experiment helps to investigate the effect of flakiness on the number of generated valid patches by a state of the art probabilistic program repair approach.
#### Experiment
```
0: Foreach Project p in [arja_project_list]:
1:      For nfr from 0 to 0,1:
2:          For 10 repetitions:
3:              Inject_flakiness(p,nfr)
4:              run_arja()
5:              record_valid_patches
```
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
