#!/bin/bash

FILES_DIR="." 

if [[ -z "$1" ]]; then
  echo "Usage: $0 <service>"
  exit 1
fi

service="$1"

file=$(find "$FILES_DIR" -type f -name "service-$1*.out")

if [[ -z "$file" ]]; then
  echo "[-] No matching .out file found for service: $service"
  exit 1
fi

echo "[+] Filtering results for service: $service"
grep "open" -B 4 "$file" || echo "[-] No open ports found in $file"
