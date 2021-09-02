# Execution Scripts

This folder is composed of different scripts and archives whose role are described bellow:

## Description

- `extract-*.sh` : Because of the large size fo the projects and the data, they have been compressed using 7zip which offers (according to our experiments) the best compression ratio. 

- `run-arja*.sh` : These scripts allow to run the probabilistic program repair using [ARJA](https://github.com/yyxhdy/arja). The script annotated by `-all` allows to run the experiment on all the targeted projects with 1 command using slurm.

- `run-pit*.sh` : These scripts allow to run the mutation testing experiment using a [forked version of pitest](https://github.com/UL-SnT-Serval/pitest.git). The script annotated by `-all` allows to run the experiment on all the targeted projects with 1 command.

- `run-prapr*.sh` : These scripts allow to run the deterministic program repair using [PR-APR](https://github.com/prapr/prapr). The script annotated by `-all` allows to run the experiment on all the targeted projects with 1 command.

- `run-sbfl*.sh` : These scripts allow to run SBFL using the [gzoltar](https://github.com/GZoltar/gzoltar). The script annotated by `-all` allows to run the experiment on all the targeted projects with 1 command command using slurm.

## Requirements

- Java version : `8 Update 2xx` with `JAVA_HOME` environment variable set (e.g., `$: export JAVA_HOME=/usr/jdk/jdk1.8.0_271`)
- Apache Maven version : `3.6.3`
- **Extract the project archives** contained in `\projects\` using `run\extract-projects.sh`.

## Run scripts

1. ```cd /run/```
2. ./<name_script>.sh arg1 arg2