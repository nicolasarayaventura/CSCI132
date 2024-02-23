#!/usr/bin/env python3
#Author:Nicolas Araya Ventura
#Created on : Nov,18 ,2023
#Description: pdb (Project )
import sys

class PDBHistogram:
    def __init__(self, filename):
        self.filename = filename
        self.start_line, self.end_line = self.get_atom_lines()

    def get_atom_lines(self):
        with open(self.filename, 'r') as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                if line.startswith("ATOM"):
                    start_line = i
                    break
            for i in range(len(lines) - 1, -1, -1):
                if lines[i].startswith("ATOM"):
                    end_line = i
                    break
        return start_line, end_line

    def total_atoms(self):
        return self.end_line - self.start_line + 1

    def atom_histogram(self):
        atom_counts = {}
        with open(self.filename, 'r') as file:
            lines = file.readlines()
            for line in lines[self.start_line:self.end_line + 1]:
                atom_name = line.split()[11]
                if atom_name in atom_counts:
                    atom_counts[atom_name] += 1
                else:
                    atom_counts[atom_name] = 1
        return atom_counts

    def residue_histogram(self):
        residue_counts = {}
        with open(self.filename, 'r') as file:
            lines = file.readlines()
            for line in lines[self.start_line:self.end_line + 1]:
                residue_name = line.split()[3]
                if residue_name in residue_counts:
                    residue_counts[residue_name] += 1
                else:
                    residue_counts[residue_name] = 1
        return residue_counts

    def atom_info(self, element_symbols):
        serial_numbers = {}
        with open(self.filename, 'r') as file:
            lines = file.readlines()
            for line in lines[self.start_line:self.end_line + 1]:
                elements = line.split()
                atom_name = elements[11]
                atom_serial_number = elements[1]
                if atom_name in element_symbols:
                    if atom_name in serial_numbers:
                        serial_numbers[atom_name].append(atom_serial_number)
                    else:
                        serial_numbers[atom_name] = [atom_serial_number]
        return serial_numbers

    def residue_info(self, residue_names):
        serial_numbers = {}
        with open(self.filename, 'r') as file:
            lines = file.readlines()
            for line in lines[self.start_line:self.end_line + 1]:
                elements = line.split()
                residue_name = elements[3]
                atom_serial_number = elements[1]
                if residue_name in residue_names:
                    if residue_name in serial_numbers:
                        serial_numbers[residue_name].append(atom_serial_number)
                    else:
                        serial_numbers[residue_name] = [atom_serial_number]
        return serial_numbers

if len(sys.argv) != 2:
    print("Usage: ./pdb_histogram.py <filename>")
    sys.exit(1)

pdb_histogram = PDBHistogram(sys.argv[1])

while True:
    print("Welcome to the 'PDB' Histogram program")
    print(f"File under reference: {sys.argv[1]}")
    print("To begin, try typing 'help' for the list of valid commands.")

    command = input("Enter Command: ")

    if command == "quit":
        break
    elif command == "help":
        print("___Command____________________Info & Usage___")
        print("total                 - Identify how many distinct atoms")
        print("                       Usage: <total>")
        print("")
        print("atomhistogram         - Display each distinct atom that was stored")
        print("                       Usage: <atomhistogram>")
        print("")
        print("reshistogram          - Display each distinct residue by the atom")
        print("                       Usage: <reshistogram>")
        print("")
        print("atominfo              - Report the count of atoms of that element, and the serial number of those atoms.")
        print("                       Usage: <atominfo element_symbols>")
        print("                       Example: <atominfo C N>")
        print("")
        print("residueinfo           - Report the count of atoms of that residue, and the serial number of those atoms.")
        print("                       Usage: <residueinfo residue_names>")
        print("                       Example: <residueinfo CYS GLY>")
        print("quit                  - Exit Program!")
        print("")
    elif command == "total":
        print(f"{pdb_histogram.total_atoms()} atoms in file {sys.argv[1]}")
    elif command == "atomhistogram":
        atom_counts = pdb_histogram.atom_histogram()
        for atom, count in atom_counts.items():
            print(f"{atom}\t{count}")
    elif command == "reshistogram":
        residue_counts = pdb_histogram.residue_histogram()
        for residue, count in residue_counts.items():
            print(f"{residue}\t{count}")
    elif command.startswith("atominfo"):
        element_symbols = command.split()[1:]
        serial_numbers = pdb_histogram.atom_info(element_symbols)
        for atom, numbers in serial_numbers.items():
            print(f"Here are the serial numbers for the element {atom}: {' '.join(numbers)}")
    elif command.startswith("residueinfo"):
        residue_names = command.split()[1:]
        serial_numbers = pdb_histogram.residue_info(residue_names)
        for residue, numbers in serial_numbers.items():
            print(f"Here are the serial numbers for {residue}: {' '.join(numbers)}")
    else:
        print("Invalid command. Type 'help' for a list of valid commands.")
