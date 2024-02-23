#Author:Nicolas Araya Ventura
#Created on : Nov,18 ,2023
#Description: pdb (Project )
#!/bin/bash

# Display
while true; do
echo -e "Welcome to the 'PDB' Histogram program"

# Check if the file contains 'ATOM' lines
if ! grep -q '^ATOM' "$1"; then
    echo "Error: The file does not contain 'ATOM' lines."
    exit 1
fi

echo -e "File under reference: $1"

echo -e "To begin, try typing 'help' for the list of valid commands."

# Commands
read -p "Enter Command: " command
case $command in
    "quit" )
        exit 0
    ;;
    "help") # try making a table with command and info towards command
        echo -e "___Command____________________Info & Usage___"
        echo -e "total                 -Identify how many distinct atoms"
        echo -e "                      Usage: <total>"
        echo -e ""
        echo -e "atomhistogram         -Display each distinct atom that was stored"
        echo -e "                      Usage: <atomhistogram>"
        echo -e ""
        echo -e "reshistogram          -Display each distinct residue by the atom"
        echo -e "                      Usage: <reshistogram>"
        echo -e ""
        echo -e "atominfo              -Report the count of atoms of that element, and the serial number of those atoms."
        echo -e "                      Usage: <atominfo element_symbols>"
        echo -e "                      Example: <atominfo C N>"
        echo -e ""
        echo -e "residueinfo           -Report the count of atoms of that residue, and the serial number of those atoms."
        echo -e "                      Usage: <residueinfo residue_names>"
        echo -e "                      Example: <residueinfo CYS GLY>"
        echo -e "quit                  -Exit Program!"
        echo ""
        echo ""
    ;;
    "total")
        # Find the total count of 'ATOM' lines in the file
        total_atoms=$(grep -c '^ATOM' "$1")
        # Display the result along with some debugging information
        echo ""
        echo "$total_atoms atoms in file $1"
        echo ""
    ;;

    "atomhistogram")
        # find start and stop pos using 'ATOM'
        start_line=$(grep -n '^ATOM' "$1" | head -n 1 | cut -d: -f1)
        end_line=$(grep -n '^ATOM' "$1" | tail -n 1 | cut -d: -f1)

        # atom histogram
        awk -v start="$start_line" -v end="$end_line" 'NR >= start && NR <= end { print $12 }' "$1" | sort | uniq -c | sort -nr | awk '{ printf "%s\t%s\n", $2, $1 }'
    ;;
    "reshistogram")
        # Find the first and last line numbers with lines starting with 'ATOM'
        start_line=$(grep -n '^ATOM' "$1" | head -n 1 | cut -d: -f1)
        end_line=$(grep -n '^ATOM' "$1" | tail -n 1 | cut -d: -f1)

        # Process lines between start_line and end_line
        awk -v start="$start_line" -v end="$end_line" 'NR >= start && NR <= end { print $4 }' "$1" | sort | uniq -c | sort -nr | awk '{ printf "%s\t%s\n", $2, $1 }'

        # Note: The above line generates a histogram of the counts for the 4th column

        # If you also want to display the count, you can add the following line
        count=$(awk -v start="$start_line" -v end="$end_line" 'NR >= start && NR <= end { count++ } END { print count }' "$1")
        echo "Total count: $count"
    ;;
    "atominfo")
        # Find the first and last line numbers with lines starting with 'ATOM'
        start_line=$(grep -n '^ATOM' "$1" | head -n 1 | cut -d: -f1)
        end_line=$(grep -n '^ATOM' "$1" | tail -n 1 | cut -d: -f1)

        # Check if the file contains 'ATOM' lines
        if [[ -z $start_line || -z $end_line ]]; then
            echo "Error: The file does not contain 'ATOM' lines."
            exit 1
        fi

        # Prompt user to enter a list of element symbols separated by spaces
        read -p "Enter a list of element symbols separated by spaces: " element_list

        # Check if the element list is provided
        if [[ -z $element_list ]]; then
            echo "Error: No element symbols provided."
            exit 1
        fi

        # Process lines between start_line and end_line
        for element_symbol in $element_list; do
            declare -a col2_array
            found_serial_numbers=false
            
            while IFS= read -r line; do
                if [[ $line =~ ^ATOM && $(echo "$line" | awk '{print $12}') == "$element_symbol" ]]; then
                    col2_array+=($(echo "$line" | awk '{print $2}'))
                    found_serial_numbers=true
                fi
            done < <(sed -n "${start_line},${end_line}p" "$1")
            
            # Display the integers on the same line
            if [ "$found_serial_numbers" = true ]; then
                echo -n "Here are the serial numbers for the element $element_symbol: "
                echo -n "${col2_array[@]}" | tr ' ' ' '
                echo  # Move to the next line for the next element symbol
            else
                echo "Error: No serial numbers found for the element '$element_symbol'."
            fi
        done
    ;;
    "residueinfo")
        # Find the first and last line numbers with lines starting with 'ATOM'
        start_line=$(grep -n '^ATOM' "$1" | head -n 1 | cut -d: -f1)
        end_line=$(grep -n '^ATOM' "$1" | tail -n 1 | cut -d: -f1)

        # Check if the file contains 'ATOM' lines
        if [[ -z $start_line || -z $end_line ]]; then
            echo "Error: The file does not contain 'ATOM' lines."
            exit 1
        fi

        # Prompt user to enter a list of three-letter residues separated by spaces
        read -p "Enter a list of three-letter residues separated by spaces: " residue_list

        # Check if the residue list is provided
        if [[ -z $residue_list ]]; then
            echo "Error: No residue list provided."
            exit 1
        fi

        # Process lines between start_line and end_line
        for residue_code in $residue_list; do
            found_serial_numbers=false
            echo "Here are the serial numbers for $residue_code:"
            while IFS= read -r line; do
                if [[ $line =~ ^ATOM && $(echo "$line" | awk '{print $4}') == "$residue_code" ]]; then
                    echo -n "$(echo "$line" | awk '{print $2}') "
                    found_serial_numbers=true
                fi
            done < <(sed -n "${start_line},${end_line}p" "$1")
            
            if [ "$found_serial_numbers" = false ]; then
                echo "None found."
            else
                echo  # Move to the next line for the next residue if serial numbers were found
            fi
        done
    ;;
    *)
        echo "Invalid command. Type 'help' for a list of valid commands."
    ;;
esac
done