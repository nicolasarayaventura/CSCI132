#!/usr/bin/env python3
# Author: Nicolas Araya Ventura
# Created on: Nov,16,2023
# Description: DNA Translation (Project_python)

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
        # Concatenate lines and filter DNA characters
        dna_sequence = ''.join(''.join(re.findall('[ACTGactg]', line)) for line in file.readlines()).upper()
except FileNotFoundError:
    print(f"Cannot open {sys.argv[1]} for reading")
    sys.exit(1)

# Set start and Stop codon
start_codon = Amino_Acids["Met"]
stop_codons = [Amino_Acids["stop1"], Amino_Acids["stop2"], Amino_Acids["stop3"]]

# Initialize variables to store codons and amino acids
codons = []
amino_sequence = ""

# Process the DNA sequence in groups of 3
for i in range(0, len(dna_sequence), 3):
    codon = dna_sequence[i:i + 3]
    codons.append(codon)
    
    # Check for start and stop codons
    if codon == start_codon:
        print("Found start codon")
    elif codon in stop_codons:
        print("Found stop codon")
        break  # Stop reading after the first stop codon
    
    # Translate codons to amino acids
    for amino, codons_list in Amino_Acids.items():
        if codon in codons_list.split(','):
            if amino.startswith("stop"):
                break
            amino_sequence += amino + " "
            break
# Display
print(f"File: {sys.argv[1]}")
print("Codon Sequence:")
print(' '.join(codons))
codon_count = len(codons)
base_count = codon_count * 3 
print(f"\n\nAmino Acid Sequence:\n{amino_sequence.strip()}\n\nNumber of Codons Displayed: {codon_count}\nNumber of Bases Displayed: {base_count}\n")

# Display Amino Acid Counts
print("Amino Acid Counts:")
counted_amino_acids = set()

for amino in Amino_Acids:
    if amino.startswith("stop"):
        continue
    
    count = amino_sequence.split().count(amino)
    if count > 0:
        print(f"{amino} {count}")
        counted_amino_acids.add(amino)

print(f"\nThey're {len(counted_amino_acids)} different Amino acids!")
