#!/bin/bash

filename="*txt"

for file in $filename
do
 echo "Contents of $file"
 echo "---"
 cat "$file"
 echo
done
