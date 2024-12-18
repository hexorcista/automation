#!/bin/bash

if [[ $# -ne 3 ]]; then
    echo "Usage: $0 <IP_list_file> <output_file> <protocol>"
    exit 1
fi

INPUT_FILE="$1"
OUTPUT_FILE="$2"
PROTOCOL="$3"

if [[ ! -f "$INPUT_FILE" ]]; then
    echo "Error: Input file '$INPUT_FILE' not found."
    exit 1
fi

while IFS= read -r IP; do
    echo "Processing IP: $IP"

    echo "SMB scan results for $IP:" >> "$OUTPUT_FILE"

    if ! crackmapexec smb "$IP" >> "$OUTPUT_FILE" 2>&1; then
        echo "Error scanning $IP. Skipping..." >> "$OUTPUT_FILE"
    fi
    
    echo "Results for $IP saved."
done < "$INPUT_FILE"

echo "All IPs processed. Results are in '$OUTPUT_FILE'."
