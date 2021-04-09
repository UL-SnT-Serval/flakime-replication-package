#!/bin/bash

project=$1
bug_id=$2
flake_rate=$3
flake_strategy=$4
repetition=${5:-10}

classpath="${ARJADIR}/lib/*:${ARJADIR}/bin"
results="${WORKDIR}/results/${project}/${bug_id}/${flake_rate}/${flake_strategy}"
project_dir="${results}/project"

#setup working space
mkdir -p ${results}

rm -rf ${results}/*
cp -rf ${ARJADIR}/external ${results}/external
cp -rf ${WORKDIR}/defects4j/${project}/${bug_id} ${project_dir}

#compile code with flakime
#note that that the project needs to have the flakime plugin in its pom.xml
pushd ${project_dir}
mvn clean verify -DskipTests -Dflakime.flakeRate=${flake_rate} -Dflakime.strategy=${flake_strategy}
mvn dependency:copy-dependencies
popd

pushd ${results}

str=`echo ${project_dir}/target/dependency/*`
DEPENDENCIES=${str// /:}


#run analysis with Arja
for i in `seq 1 ${repetition}`;
do
	cmd="java -cp ${classpath} us.msu.cse.repair.Main Arja \
		-DsrcJavaDir ${project_dir}/src/ \
		-DbinJavaDir ${project_dir}/target/classes/ \
		-DbinTestDir ${project_dir}/target/test-classes/ \
		-Ddependences ${DEPENDENCIES} \
		-DpatchOutputRoot patch_${project}_${bug_id}_${flake_rate}_${flake_strategy}_${i}"

	echo ${cmd}
	$cmd > "${project}_${bug_id}_${flake_rate}_${flake_strategy}_${i}.log"
done

#clean up working space
rm -rf ${results}/external
rm -rf ${project_dir}
rm ${results}/FUN_NSGAII

popd
