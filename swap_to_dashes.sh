#!/bin/bash

# Define the directory to be searched
DIR="/Users/jdorsheimer/Projects/BioData_Catalyst/dbGaP-23523/Studies/LUNGMap_phs001961/JSON-cleaned"

# Use the find command to find all files in the directory and its subdirectories
find "$DIR" -type f | while read -r file
do
    # Use the basename and dirname commands to separate the file name from the path
    filename=$(basename "$file")
    dir=$(dirname "$file")

    # Use the tr command to replace '/' with '-' in the file name
    newfilename=$(echo "$filename" | tr '/' '-')

    # Check if the file name has been changed
    if [ "$filename" != "$newfilename" ]
    then
        # Use the mv command to rename the file
        mv "$file" "$dir/$newfilename"
    fi
done
