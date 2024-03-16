#!/bin/bash

# Check if input file is provided as argument
if [ -z "$1" ]; then
    echo "Usage: $0 <input_file>"
    exit 1
fi

# Read input file line by line
while IFS=' ' read -r file_url target_folder || [ -n "$file_url" ]; do
    # Download the file
    wget "$file_url"

    # Get the filename from the URL
    filename=$(basename "$file_url")

    # Extract folder name without extension
    foldername="${target_folder%.*}"

    # Unzip the file into a folder
    unzip "$filename" -d "$foldername"

    echo "Downloaded and extracted $filename to folder: $foldername"

    # Delete archived folder if specified
    if [ "$delete_archived_folder" = true ]; then
        rm -rf "$filename" # Remove the archived folder
        echo "Deleted archived folder: $filename"
    fi

done < "$1"
