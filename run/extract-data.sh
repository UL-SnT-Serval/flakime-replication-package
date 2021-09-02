#!/bin/bash -l

export DATA=$PWD/../data

find ${DATA} -name "*7z" -print0 | while read -d $'\0' zip_file
do
    output_folder=$(echo ${zip_file%.*})
    if [[ ! -d "$output_folder" ]]
    then
        pushd "$(dirname "$zip_file")"
        7za x $(basename $zip_file)
        popd
    else
        echo "$output_folder already exists, nothing to do."
    fi
done