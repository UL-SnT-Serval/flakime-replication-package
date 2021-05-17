#!/bin/bash -l

#SBATCH -n 4
#SBATCH -N 1
#SBATCH -c 4
#SBATCH -J arja

project=$1
bug_id=$2
flake_rate=$3
flake_strategy=$4
repetition=${5:-10}

classpath="${ARJADIR}/lib/*:${ARJADIR}/bin"
results="${WORKDIR}/data/apr/arja/${project}/${bug_id}/${flake_rate}/${flake_strategy}"
project_dir="${results}/project"

#setup working space
mkdir -p ${results}

rm -rf ${results}/*
cp -rf ${ARJADIR}/external ${results}/external
cp -rf ${WORKDIR}/defects4j/${project}/${bug_id} ${project_dir}


for i in `seq 1 ${repetition}`;
do
	key="${project}_${bug_id}_${flake_rate}_${flake_strategy}_${i}"
	mkdir "${results}/flakes_${key}"
	
	#compile code with flakime
	#note that that the project needs to have the flakime plugin in its pom.xml
	pushd ${project_dir}
	mvn clean verify \
		-DskipTests \
		-Dflakime.flakeRate=${flake_rate} \
		-Dflakime.disableReport=true \
		-P arja-${flake_strategy}
		
	mvn dependency:copy-dependencies
	popd

	pushd ${results}

	str=`echo ${project_dir}/target/dependency/*`
	DEPENDENCIES=${str// /:}

	#run analysis with Arja
	cmd="java -cp ${classpath} us.msu.cse.repair.Main Arja \
		-DsrcJavaDir ${project_dir}/src/ \
		-DbinJavaDir ${project_dir}/target/classes/ \
		-DbinTestDir ${project_dir}/target/test-classes/ \
		-Ddependences ${DEPENDENCIES} \
		-DpatchOutputRoot patch_${key}"

	echo ${cmd}
	$cmd > "${key}.log"
done

#clean up working space
rm -rf ${results}/external
#rm -rf ${project_dir}
rm ${results}/FUN_NSGAII

popd
