#!/bin/bash -l

export WORKDIR=$PWD
export ARJADIR=$WORKDIR/projects/arja

export MAVEN_OPTS=-Xss10M
export M2_REPOSITORY=$HOME/.m2/repository

mode=$1

run()
{
	PROJECT=$1
	BUG=$2

	for FLAKE_RATE in 0.00 0.01 0.02 0.03 0.04 0.05 0.06 0.07 0.08 0.09 0.10
	do
		for FLAKE_STRATEGY in vocabulary
		do
            if [ $mode == 'sbatch' ]
            then
                sbatch --output=sbfl-${PROJECT}-${BUG}-${FLAKE_RATE}-${FLAKE_STRATEGY}.out \
                --time=0-10:00:00
                ./run-sbfl.sh ${PROJECT} ${BUG} ${FLAKE_RATE} ${FLAKE_STRATEGY} 
            else
                ./run-sbfl.sh ${PROJECT} ${BUG} ${FLAKE_RATE} ${FLAKE_STRATEGY}
            fi
		done
	done
}

run lang 20 
run lang 22
run lang 39

run math 5
run math 22
run math 39
run math 50
run math 53
run math 58
run math 70
run math 98
