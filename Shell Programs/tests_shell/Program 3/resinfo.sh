#!/bin/bash

# Find the first and last line numbers with lines starting with 'ATOM'
start_line=$(grep -n '^ATOM' "$1" | head -n 1 | cut -d: -f1)
end_line=$(grep -n '^ATOM' "$1" | tail -n 1 | cut -d: -f1)

# Check if the file contains 'ATOM' lines
if [[ -z $start_line || -z $end_line ]]; then
    echo "Error: The file does not contain 'ATOM' lines."
    exit 1
fi

# Prompt user to enter a three-letter residue
read -p "Enter a three-letter residue code: " residue_code

# Check if the residue code is provided
if [[ -z $residue_code || ${#residue_code} -ne 3 ]]; then
    echo "Error: Invalid or no residue code provided. Please enter a three-letter residue code."
    exit 1
fi

# Declare an array to store column 2 values
declare -a col2_array

# Process lines between start_line and end_line
while IFS= read -r line; do
    if [[ $line =~ ^ATOM && $(echo "$line" | awk '{print $4}') == "$residue_code" ]]; then
        col2_array+=($(echo "$line" | awk '{print $2}'))
    fi
done < <(sed -n "${start_line},${end_line}p" "$1")

# Check if the residue is not present in the file
if [[ ${#col2_array[@]} -eq 0 ]]; then
    echo "Error: The residue '$residue_code' is not present in the file."
    exit 1
fi

# Display the integers on the same line
echo -n "${col2_array[@]}" | tr ' ' ' '
