#!/bin/bash

project=$1
bug_id=$2
junit=$3

classpath="${ARJADIR}/lib/*:${ARJADIR}/bin"
results="${WORKDIR}/results/${project}/${bug_id}"
project_dir="${results}/project"

#setup working space
mkdir -p ${results}

rm -rf ${results}/*
cp -rf ${ARJADIR}/external ${results}/external
cp -rf ${WORKDIR}/defects4j/${project}/${bug_id} ${project_dir}

pushd ${results}

#run analysis
cmd="java -cp ${classpath} us.msu.cse.repair.Main Arja \
	-DsrcJavaDir ${project_dir}/src/ \
	-DbinJavaDir ${project_dir}/target/classes/ 
	-DbinTestDir ${project_dir}/target/test-classes/ \
	-Ddependences ${M2_REPOSITORY}/junit/junit/${junit}/junit-${junit}.jar:${M2_REPOSITORY}/org/easymock/easymock/2.5.2/easymock-2.5.2.jar"

echo ${cmd}
$cmd > "${project}_${bug_id}.log"

#clean up working space
rm -rf ${results}/external
rm -rf ${project_dir}
rm ${results}/FUN_NSGAII
