#!/bin/bash

# Check if a file was passed as an argument
if [ -z "$1" ]; then
    echo "Usage: $0 <file_with_ips>"
    exit 1
fi

# Read the file passed as the argument
input_file="$1"

# Check if the file exists
if [ ! -f "$input_file" ]; then
    echo "File not found!"
    exit 1
fi

# Extract IP addresses and save to a new file
grep -oE '([0-9]{1,3}\.){3}[0-9]{1,3}' "$input_file" > extracted_ips.txt

# Display the extracted IPs
cat extracted_ips.txt
