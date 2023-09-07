#!/bin/bash

# # Define the files you want to process
file1="../_build/html/docs/cluster_annotations/README.html"
file2="../_build/html/docs/gene_lists/README.html"
file3="../_build/html/docs/parcellation_annotations/README.html"

# Define the sed command
sed_command='s/<a class="reference download internal" download=""/<a/g; s/<span class="xref download myst"/<span/g'

# Loop through the files and execute the sed command
for file in "$file1" "$file2" "$file3"
do
    sed -i.bak "$sed_command" "$file"
    echo "Processed $file"

done