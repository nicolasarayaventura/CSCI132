# CSCI132
 Practical UNIX and Programming
# Table of Contents
 * [Description](#Description)
 * [Programs](#programs)
 * [DNA Translation](#dna-translation)
 * [Genomic Variations Search: For Motifs in DNA](#genomic-variations-search-for-motifs-in-dna)
 * [PDB Hisotgram](#pdb-histogram)
 ## Description 
 * Project displays three seperate programs achieving different ways to extract, organize, and display data to user under different constrictions. Each project is written in either shell or python 3.
 ## Programs
 * DNA Translation
 * Genomic Variations: Search for Motifs in DNA
 * PDB Histogram

### DNA Translation
    
Purpose:

 * Demonstration of DNA translation by using shell/python

Usage:

 Running program in shell:
 
 `./prog_1_dna_translation.sh dna_file`

 Running program in python3:

 `./prog_1_dna_translation.sh dna_file`

Constraints:  

1. Directionality of DNA
2. Central Dogma of Biology
3. DNA Codons
4. Start and Stop codons
5. Pathname of 'DNA' file is only command line argument, text file or FASTA file.
6. File must contain DNA string with no new line characters or white space characters of any kind within it

### Genomic Variations: Search for Motifs in DNA
Purpose:

 * Display of the short recurring patterns in DNA from two or more different files

Usage: 

 Running program in shell:
 
 `./prog_2_gsv.sh reference_file file2 [file3...]`

 Running program in python3:

  `./prog_2_gsv.py reference_file file2 [file3...]`

 Python3 Version:
 
 * '+' indicates that the motif is present only in the file being compared (not in the reference file).
 * '-' indicates that the motif is present only in the reference file (not in the comparison file).
 * '?' indicates that the comparison is inconclusive due to an ambiguous difference between the reference and comparison files.
 * '^' marks the position in the motif where the difference occurs.

Motifs from the reference file and the comparison file are aligned side by side, separated by tabs.
  
Constraints:  

1. Directionality of DNA
2. Central Dogma of Biology
3. DNA Codons
4. Start and Stop codons
5. Pathname of 'DNA' file is only command line argument, text file or FASTA file.
6. File must contain DNA string with no new line characters or white space characters of any kind within it
   
### PDB Histogram
Purpose:
 * A program to extract needed information to a user from a Protein Data Bank File
Usage:

 Running program in shell:
 
`./prog_3_pdb.sh reference_file file2 [file3...]`

 Running program in python3: 

 `./prog_3_pdb.py reference_file file2 [file3...]`
 
Constraints:  
 1. PDB Files
 2. File Reading
