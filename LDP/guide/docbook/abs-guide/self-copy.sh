#!/bin/bash
# self-copy.sh

# This script copies itself.

file_subscript=copy

dd if=$0 of=$0.$file_subscript 2>/dev/null
# Suppress messages from dd:   ^^^^^^^^^^^

exit $?
