#!/bin/bash -l

#SBATCH -n 1
#SBATCH -N 1
#SBATCH -c 2
#SBATCH -J sbfl

project=$1
bug_id=$2
flake_rate=$3
flake_strategy=$4
repetition=${5:-10}

results="${WORKDIR}/data/sbfl/${project}/${bug_id}/${flake_rate}/${flake_strategy}"
project_dir="${results}/project"

gzoltar="${project_dir}/target/site/gzoltar/sfl/txt"

#setup working space
mkdir -p ${results}

rm -rf ${results}/*
cp -rf ${WORKDIR}/defects4j/${project}/${bug_id} ${project_dir}

for i in `seq 1 ${repetition}`;
do	
	#compile code with flakime
	#note that that the project needs to have the flakime plugin in its pom.xml
	pushd ${project_dir}
	mvn clean test \
		-Dflakime.flakeRate=${flake_rate} \
		-Dflakime.disableReport=true \
		-Dflakime.strategy=${flake_strategy} \
        -P sbfl
	popd

	cp ${gzoltar}/ochiai.ranking.csv ${results}/ochiai-$i.csv
	cp ${gzoltar}/dstar.ranking.csv ${results}/dstar-$i.csv
	cp ${gzoltar}/tarantula.ranking.csv ${results}/tarantula-$i.csv
	cp ${gzoltar}/barinel.ranking.csv ${results}/barinel-$i.csv
done

#clean up working space
rm -rf ${project_dir}
