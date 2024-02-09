#!/bin/bash

# Find the first and last line numbers with lines starting with 'ATOM'
start_line=$(grep -n '^ATOM' "$1" | head -n 1 | cut -d: -f1)
end_line=$(grep -n '^ATOM' "$1" | tail -n 1 | cut -d: -f1)

# Process lines between start_line and end_line
awk -v start="$start_line" -v end="$end_line" 'NR >= start && NR <= end { print $12 }' "$1" | sort | uniq -c | sort -nr | awk '{ printf "%s\t%s\n", $2, $1 }'

# Note: The above line generates a histogram of the counts for the 12th column

# If you also want to display the count, you can add the following line
count=$(awk -v start="$start_line" -v end="$end_line" 'NR >= start && NR <= end { count++ } END { print count }' "$1")
echo "Total count: $count"
