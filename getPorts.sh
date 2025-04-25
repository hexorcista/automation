#!/bin/bash

# Usage: ./extract_ports.sh <nmapScanOutFile>
# This script help to perform more efficient scans to specific ports identified by just a portscan on the targets
# We can save time when performing the service version scans or script scans.

if [ -z "$1" ]; then
  echo "Usage: $0 <input_file>"
  exit 1
fi

ports=$(grep -oP '^\d+/tcp' "$1" | cut -d'/' -f1 | sort -n | uniq)
output=$(echo "$ports" | paste -sd, -)
echo "$output"
