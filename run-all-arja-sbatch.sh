#!/bin/bash -l

run()
{
	PROJECT=$1
	BUG=$2

	for FLAKE_RATE in 0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0
	do
		for FLAKE_STRATEGY in vocabulary uniformDistribution
		do
			sbatch --output=arja-${PROJECT}-${BUG}-${FLAKE_RATE}-${FLAKE_STRATEGY}.out \
				   --time=0-10:00:00
				   ./run-arja-sbatch.sh ${PROJECT} ${BUG} ${FLAKE_RATE} ${FLAKE_STRATEGY} 
		done
	done
}

run lang 20 