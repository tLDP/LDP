#!/bin/bash

{
read fstab
} < /etc/fstab

echo "First line in /etc/fstab is:"
echo "$fstab"

exit 0
