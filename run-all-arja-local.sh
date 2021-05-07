#!/bin/bash -l

run()
{
	PROJECT=$1
	BUG=$2

	for FLAKE_RATE in 0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0
	do
		for FLAKE_STRATEGY in vocabulary uniformDistribution
		do
			./run-arja-local.sh ${PROJECT} ${BUG} ${FLAKE_RATE} ${FLAKE_STRATEGY} 
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