#!/bin/bash

FILES_DIR="." 

if [[ -z "$1" ]]; then
  echo "Usage: $0 <service>"
  echo "Example: $0 mysql"
  exit 1
fi

service="$1"

file=$(find "$FILES_DIR" -type f -name "*.out")

if [[ -z "$file" ]]; then
  echo "[-] No matching .nmap file found for service: $service"
  exit 1
fi

echo "[+] Filtering results for service: $service"
grep "open" -B 4 "$file" || echo "[-] No open ports found in $file"
