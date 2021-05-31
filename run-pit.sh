#!/bin/bash
flakeRate=$2
custom_javahome=/usr/jdk/jdk1.8.0_271
project_dir=$1


if [ $# -lt 2 ]; then
    echo "please provide {projectdir} {flakerate}"
    exit 1;
fi


if [ ! -d $project_dir ]; then
    echo "Project directory should be provided and present."
    exit 1
fi

if [ ! -d $custom_javahome ]; then
    echo "Incorrect java_home."
    exit 1
fi

cd $project_dir

# echo "Flake rate [${flakeRate}]"
for i in {1..10}
do
    echo "####################### [i:$i/10][fr: ${flakeRate}][${project_dir}]"
    MAVEN_OPTS=-Xss10m JAVA_HOME=$custom_javahome mvn -Drat.skip=true clean test-compile \
                        -Dflakime.flakeRate=${flakeRate} \
                        -Dflakime.strategy=vocabulary;
    echo "Build finish running mutation."
    JAVA_HOME=/usr/java/jdk1.8.0_281 mvn org.pitest:pitest-maven:mutationCoverage;
    total_flake=$(wc -l target/flakime/* | grep -E 'total');
    total_killed=$(grep -E 'KILLED|TIMED_OUT' target/pit-reports/**/mutations.csv | wc -l);
    total_gen=$(grep -E '' target/pit-reports/**/mutations.csv | wc -l);
    str="${i},${total_gen},${total_flake},${total_killed}";
    echo "${str}";
    echo "${str}" >> output_$flakeRate.out;
done

