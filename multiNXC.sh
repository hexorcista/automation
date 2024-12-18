#!/bin/bash

if [[ $# -ne 2 ]]; then
    echo "Usage: $0 <IP_list_file> <output_file>"
    exit 1
fi

INPUT_FILE="$1"
OUTPUT_FILE="$2"

if [[ ! -f "$INPUT_FILE" ]]; then
    echo "Error: Input file '$INPUT_FILE' not found."
    exit 1
fi

> "$OUTPUT_FILE"

while IFS= read -r IP; do
    echo "Processing IP: $IP"
    
    crackmapexec smb "$IP" >> "$OUTPUT_FILE"
    
    echo "Results for $IP saved."
done < "$INPUT_FILE"

echo "All IPs processed. Results are in '$OUTPUT_FILE'."
