#!/bin/bash
# Reading lines in /etc/fstab.

{
read line1
read line2
} < /etc/fstab

echo "First line in /etc/fstab is:"
echo "$line1"
echo
echo "Second line in /etc/fstab is:"
echo "$line2"

exit 0
