#!/bin/bash -l

export WORKDIR=$PWD/..
export MAVEN_OPTS=-Xss10M

mode=$1

run() #$1 is the project directory ; $2 is the defect4j bug id
{
	PROJECT=$1
	BUG=$2

	for FLAKE_RATE in 0.0 0.05 0.1 0.15 0.2 0.25 0.3 0.35 0.4 0.45 0.5
	do
      ./run-pit.sh ${PROJECT} ${FLAKE_RATE}  
    done
}

run current/jfreechart
run current/commons-math
run current/commons-lang
run current/joda-time