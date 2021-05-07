#!/bin/bash -l

run()
{
	PROJECT=$1
	BUG=$2

	for FLAKE_RATE in 0.00 0.01 0.02 0.03 0.04 0.05 0.06 0.07 0.08 0.09 0.10
	do
		for FLAKE_STRATEGY in vocabulary
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

