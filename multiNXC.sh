#!/bin/bash

if [[ $# -ne 3 ]]; then
    echo "Usage: $0 <IP_list_file> <protocol> <output_file>"
    exit 1
fi

INPUT_FILE="$1"
PROTOCOL="$2"
OUTPUT_FILE="$3"

if [[ ! -f "$INPUT_FILE" ]]; then
    echo "Error: Input file '$INPUT_FILE' not found."
    exit 1
fi

> "$OUTPUT_FILE"

while IFS= read -r IP; do
    echo "Processing IP: $IP with protocol: $PROTOCOL"

    echo "Results for IP $IP using protocol $PROTOCOL:" >> "$OUTPUT_FILE"

    if ! nxc "$PROTOCOL" "$IP" >> "$OUTPUT_FILE" 2>&1; then
        echo "Error processing IP $IP. Skipping..." >> "$OUTPUT_FILE"
    fi

    echo "----------------------------------------" >> "$OUTPUT_FILE"

    echo "Finished processing $IP."
done < "$INPUT_FILE"

echo "All IPs processed. Results are in '$OUTPUT_FILE'."
