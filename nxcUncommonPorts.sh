#!/bin/bash

# File Input Format Expected:
# <port> <IP>
if [ -z "$4" ]; then
  echo "Usage: $0 <input_file> <protocol> <user/userList> <password/passwordList>"
  exit 1
fi

input_file="$1"
protocol="$2"
user=$3
password=$4

if [ ! -f "$input_file" ]; then
  echo "File not found!"
  exit 1
fi

while read -r port ip; do
  nxc $protocol $ip -u $user -p $password --port $port $auth # add or remove flags as needed
done < "$input_file"
