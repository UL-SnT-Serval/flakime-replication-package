#!/bin/bash

export WORKDIR=/mnt/d/workspaces/flakime
export ARJADIR=/mnt/d/projects/arja

export MAVEN_OPTS=-Xss10M
export M2_REPOSITORY=$HOME/.m2/repository

./arja.sh lang 20 4.7 0.5
