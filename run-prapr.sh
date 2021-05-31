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

rep=10
i=0
if [ $flakeRate == "0.0" ]; then
    rep=1;
fi

while [ $i -lt $rep ]; do
echo "####################### [i:$i/$rep] [fr: ${flakeRate}][${project_dir}]"
MAVEN_OPTS=-Xss10m JAVA_HOME=$custom_javahome \
   mvn clean -P pr-apr org.mudebug:prapr-plugin:prapr \
   -Dflakime.flakeRate=${flakeRate} \
   -Dflakime.strategy=vocabulary;
    cat target/prapr-reports/**/fix-report.log | grep -E 'Plausible Fixes' | grep -o '[0-9]*' >> $flakeRate.log
    i=$((i+1))
done