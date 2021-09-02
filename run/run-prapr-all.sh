#!/bin/bash -l

export WORKDIR=$PWD/..
export MAVEN_OPTS=-Xss10M

mode=$1

run() #$1 is the project directory ; $2 is the defect4j bug id
{
	PROJECT=$1
	BUG=$2

	for FLAKE_RATE in 0.0 0.1 0.2 0.3 0.4 0.5
	do
      ./run-prapr.sh ${PROJECT}/${BUG} ${FLAKE_RATE}  
    done
}

run defects4j/lang 6

run defects4j/mock 29
run defects4j/mock 38

run defects4j/time 11
run defects4j/time 19

run defects4j/math 5
run defects4j/math 34
run defects4j/math 50
run defects4j/math 82
run defects4j/math 85

run defects4j/mock 29
run defects4j/mock 38