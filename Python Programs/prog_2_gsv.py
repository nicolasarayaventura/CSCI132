#!/usr/bin/env python3
#Author:Nicolas Araya Ventura
#Created on : Nov,16,2023
#Description: GSV (Project_python)
import sys
import difflib

class DNAComparison:
    def __init__(self, reference_file, files_to_compare):
        self.reference_file = reference_file
        self.files_to_compare = files_to_compare
        self.motif_length = 10

    def extract_motifs(self, filename):
        with open(filename, 'r') as file:
            dna_sequence = ''.join(filter(lambda char: char in 'actgACTG', file.read().upper()))
            return [dna_sequence[i:i+self.motif_length] for i in range(0, len(dna_sequence), self.motif_length)]

    def process_file(self, reference, file):
        motifs_ref = self.extract_motifs(reference)
        motifs_file = self.extract_motifs(file)

        differences = difflib.ndiff(motifs_ref, motifs_file)
        differences_str = '\n'.join(differences)

        print(f"Reference File: {reference}")
        print(f"Comparing DNA files: {file}")
        print(f"Differences in DNA sequence motifs (length {self.motif_length}):")
        print(differences_str)

        while True:
            query = input("Use the follow commands, 'next' <next file>, 'previous' <previous file>, 'search' <search query>, 'motif'<change motif length>, or 'quit' to exit: ")

            if query == "next":
                break
            elif query == "previous":
                break
            elif query == "quit":
                sys.exit(0)
            elif query == "motif":
                new_motif_length = int(input("Enter a new motif length: "))
                print(f"Motif length updated to: {new_motif_length}")
                self.motif_length = new_motif_length
            elif query == "search":
                search_query = input("Enter a query to search in motifs: ")
                for idx, motif in enumerate(motifs_file):
                    if search_query in motif:
                        motif_start = idx * self.motif_length
                        motif_end = motif_start + self.motif_length
                        print(f"Query: {search_query} found at position: {motif.find(search_query)} in motif starting at position: {motif_start} in {file}")
            else:
                for idx, motif in enumerate(motifs_file):
                    if query in motif:
                        motif_start = idx * self.motif_length
                        motif_end = motif_start + self.motif_length
                        print(f"Query: {query} found at position: {motif.find(query)} in motif starting at position: {motif_start} in {file}")
                        break

# Check if at least 2 files are provided
if len(sys.argv) < 3:
    print("Need 2 or more files to compare. <Usage> ./gsv_dna.py reference_file file2 [file3...]")
    sys.exit(1)

reference_file = sys.argv[1]
files_to_compare = sys.argv[2:]

dna_comparison = DNAComparison(reference_file, files_to_compare)

# Loop through the files
current_file_index = 0
while True:
    current_file = dna_comparison.files_to_compare[current_file_index]
    dna_comparison.process_file(dna_comparison.reference_file, current_file)
