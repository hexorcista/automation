#!/bin/bash

# Check if a file was passed as an argument
if [ -z "$1" ]; then
    echo "Usage: $0 <file_with_ips>"
    exit 1
fi

# Read the file passed as the argument
ips_file="$1"

# Check if the file exists
if [ ! -f "$ips_file" ]; then
    echo "File not found!"
    exit 1
fi

# Loop through each line in the file and scan with rustscan
while IFS= read -r ip; do
    rustscan -a $ip  --range 1-65535 --timeout 3500 --ulimit 3000 -- -sV -sC -Pn
done < "$ips_file"
