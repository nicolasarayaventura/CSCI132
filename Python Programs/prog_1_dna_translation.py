#!/usr/bin/env python3
#Author:Nicolas Araya Ventura
#Created on : Nov,16,2023
#Description: Dna Trnaslation (Project_python)

import sys
import re

# Amino Acid Dictionary
Amino_Acids = {
    "Phe": "TTC,TTT", "Leu": "TTA,TTG,CTT,CTC,CTA,CTG",
    "Ile": "ATT,ATC,ATA", "Met": "ATG", "Val": "GTT,GTC,GTA,GTG",
    "Ser": "TCT,TCC,TCA,TCG,AGT,AGC", "Pro": "CCT,CCC,CCA,CCG",
    "Thr": "ACT,ACC,ACA,ACG", "Ala": "GCT,GCC,GCA,GCG",
    "Tyr": "TAT,TAC", "His": "CAC,CAT", "Gln": "CAA,CAG",
    "Asn": "AAT,AAC", "Lys": "AAA,AAG", "Asp": "GAT,GAC",
    "Glu": "GAA,GAG", "Cys": "TGT,TGC,TGC", "Trp": "TGG",
    "Arg": "CGT,CGC,CGA,CGG,AGA,AGG", "Gly": "GGT,GGC,GGA,GGG",
    "stop1": "TAA", "stop2": "TAG", "stop3": "TGA"
}

# Error Checks
if len(sys.argv) < 2:
    print("No file has been presented, Usage: <dnafile>")
    sys.exit(1)

try:
    with open(sys.argv[1], 'r') as file:
        codseq = ''.join(re.findall('[actgACTG]', file.read())).upper()
except FileNotFoundError:
    print(f"Cannot open {sys.argv[1]} for reading")
    sys.exit(1)

# Find start and stop positions
start_codon = Amino_Acids["Met"]
stop_codons = [Amino_Acids["stop1"], Amino_Acids["stop2"], Amino_Acids["stop3"]]
start_position = codseq.find(start_codon)

# Check if start position is found
if start_position == -1:
    print("Error: Start codon not found in the file.")
    sys.exit(1)

# Find the stop position
stop_position = None
for stop_codon in stop_codons:
    stop_pos = codseq.find(stop_codon, start_position)
    if stop_pos != -1:
        stop_position = stop_pos
        break

# Check stop position
if stop_position is None:
    print("Error: Stop codon not found after the start codon in the file.")
    sys.exit(1)

# Get sequence between start and stop codons
extracted_sequence = codseq[start_position:stop_position]

# Translate codons to amino acids
amino_sequence = ""
for i in range(0, len(extracted_sequence), 3):
    codon = extracted_sequence[i:i+3]
    for amino, codons in Amino_Acids.items():
        if codon in codons.split(','):
            if amino.startswith("stop"):
                break
            amino_sequence += amino + " "
            break

# Display
print(f"File: {sys.argv[1]}")
print("Codon Sequence:")
print(' '.join([extracted_sequence[i:i+3] for i in range(0, len(extracted_sequence), 3)]))
codon_count = len(extracted_sequence) // 3
base_count = len(extracted_sequence)
print(f"\n\nAmino Acid Sequence:\n{amino_sequence.strip()}\n\nNumber of Codons Displayed: {codon_count}\nNumber of Bases Displayed: {base_count}\n")

# Display Amino Acid Counts
print("Amino Acid Counts:")
for amino in Amino_Acids:
    if amino in amino_sequence:
        count = amino_sequence.split().count(amino)
        print(f"{amino} {count}")
print(f"\nThey're {len(amino_sequence.split())} different Amino acids!")
