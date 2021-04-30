#!/bin/bash -l

#SBATCH -n 4
#SBATCH -N 1
#SBATCH -c 4
#SBATCH -J arja

module purge

export WORKDIR=/mnt/d/workspaces/flakime
export ARJADIR=/mnt/d/projects/arja

export MAVEN_OPTS=-Xss10M
export M2_REPOSITORY=$HOME/.m2/repository

./arja.sh $1 $2 $3 $4 $5
