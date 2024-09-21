#!/bin/bash

# Check if the user has provided a file as an argument
# File Input Format Expected:
# <port> <IP>


if [ -z "$2" ]; then
  echo "Usage: $0 <input_file> <protocol>"
  exit 1
fi

input_file="$1"
protocol="$2"

if [ ! -f "$input_file" ]; then
  echo "File not found!"
  exit 1
fi

while read -r port ip; do
  nxc $protocol $ip -u '' -p '' --port $port
done < "$input_file"
