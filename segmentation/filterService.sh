#!/bin/bash

NMAP_FILES_DIR="." 

if [[ -z "$1" ]]; then
  echo "Usage: $0 <service>"
  echo "Example: $0 mysql"
  exit 1
fi

service="$1"

nmap_file=$(find "$NMAP_FILES_DIR" -type f -name "service-${service}-*.nmap")

if [[ -z "$nmap_file" ]]; then
  echo "[-] No matching .nmap file found for service: $service"
  exit 1
fi

echo "[+] Filtering results for service: $service"
grep "open" -B 4 "$nmap_file" || echo "[-] No open ports found in $nmap_file"
