#!/bin/bash -l

export WORKDIR=$PWD/..
export ARJADIR=$WORKDIR/arja

export MAVEN_OPTS=-Xss10M
export M2_REPOSITORY=$HOME/.m2/repository

mode=$1
flake_strategy="${2:-vocabulary}"

if [ ! -d "$ARJADIR" ]; then
    git clone https://github.com/anonymized/arja.git arja
    pushd $ARJADIR
    mkdir bin
    javac -cp "lib/*:" -d bin $(find src -name '*.java')
    popd
fi

run()
{
	PROJECT=$1
	BUG=$2

    if [ $flake_strategy == 'vocabulary-no-fl' ]
    then 
        flake_rates=(0.05)
    else 
        flake_rates=(0.00 0.01 0.02 0.03 0.04 0.05 0.06 0.07 0.08 0.09 0.10)
    fi

	for flake_rate in $flake_rates
	do
        if [ $mode == 'sbatch' ]
        then
            export JAVA_HOME=$HOME/bin/jdk1.8.0_291
            export PATH=$HOME/bin/jdk1.8.0_291/bin:$PATH

            sbatch --output=sbfl-${PROJECT}-${BUG}-${flake_rate}-${flake_strategy}.out \
            --time=0-10:00:00
            ./run-arja.sh ${PROJECT} ${BUG} ${flake_rate} ${flake_strategy} 
        else
            ./run-arja.sh ${PROJECT} ${BUG} ${flake_rate} ${flake_strategy}
        fi
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
