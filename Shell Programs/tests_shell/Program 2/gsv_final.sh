#!/bin/bash

# Check if at least 2 files are provided
if [ "$#" -lt 2 ]; then
    echo "Need 2 or more files to compare. <Usage> ./gsv_dna.sh reference_file file2 [file3...]"
    exit 1
fi

# Extract the reference file (the first file)
reference="$1"
shift  # Remove the reference file from the argument list

motif_length=10
file_count=$#
current_file_index=1

# Function to display differences and perform motif search
function process_file {
    file="$1"
    motifs_ref=$(awk '/^>/ {next} {gsub(/[^actgACTG]/, ""); print}' "$reference" | fold -w "$motif_length")
    motifs_file=$(awk '/^>/ {next} {gsub(/[^actgACTG]/, ""); print}' "$file" | fold -w "$motif_length")

    differences=$(diff -y <(echo "$motifs_ref") <(echo "$motifs_file"))

    echo "Reference File: $reference"
    echo "Comparing DNA files: $file"
    echo "Differences in DNA sequences motifs (length $motif_length):"
    echo "$differences"

    while true; do
        read -p "Use the follow commands, 'next' <next file>, 'previous' <previous file>, 'search' <search query>, 'motif'<change motif length>, or 'quit' to exit: " query

        case $query in
            "next")
                current_file_index=$((current_file_index % file_count + 1))
                break
                ;;
            "previous")
                current_file_index=$((current_file_index > 1 ? current_file_index - 1 : file_count))
                break
                ;;
            "quit")
                exit 0
                ;;
            "search")
                read -p "Enter a query to search in motifs: " search_query
                echo "$motifs_file" | grep -b -o -i "$search_query" | awk -v motif_length="$motif_length" -v query="$search_query" -v file="$file" '
                    { 
                        printf "Query: %s found at position: %d in motif starting at position: %d in %s\n", query, $1, int($1/motif_length)+1, file
                    }'
                ;;
            "motif")
                read -p "Enter a new motif count: " new_motif_count
                motif_length="$new_motif_count"
                echo "Motif count updated to: $motif_length"
                ;;
            *)
                # Perform the search within the motifs and display positions
                echo "$motifs_ref" | grep -b -o -i "$query" | awk -v motif_length="$motif_length" -v query="$query" -v file="$file" '
                    { 
                        printf "Query: %s found at position: %d in motif starting at position: %d in %s\n", query, $1, int($1/motif_length)+1, file
                    }'
                ;;
        esac
    done
}

# Loop through the files
while true; do
    current_file="${!current_file_index}"
    process_file "$current_file"
done
