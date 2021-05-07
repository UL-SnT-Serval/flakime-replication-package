#!/bin/bash -l

export WORKDIR=$HOME/workspaces/flakime-replication-package
export ARJADIR=$HOME/projects/arja

export MAVEN_OPTS=-Xss10M
export M2_REPOSITORY=$HOME/.m2/repository

./arja.sh $1 $2 $3 $4 $5
