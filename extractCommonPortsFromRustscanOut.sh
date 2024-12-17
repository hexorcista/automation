#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: $0 <input_file>"
    exit 1
fi

INPUT_FILE="$1"

if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: File '$INPUT_FILE' not found."
    exit 1
fi

PORTS="80 21 139 445 2049 53 25 587 110 143 3306 1433 22 5985 5986 3389 135"

OUTPUT_DIR="commonPorts"
mkdir -p "$OUTPUT_DIR"  

for PORT in $PORTS; do
    OUTPUT_FILE="${OUTPUT_DIR}/port_${PORT}.txt"
    grep -E "Open [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+:${PORT}([^0-9]|$)" "$INPUT_FILE" > "$OUTPUT_FILE"
    echo "Lines with port ${PORT} saved to '${OUTPUT_FILE}'."
done

echo "Extraction completed. Check the '$OUTPUT_DIR' directory for results."
