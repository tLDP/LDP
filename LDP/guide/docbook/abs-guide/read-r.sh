#!/bin/bash

echo

echo "Enter a string terminated by a \\, then press &lt;ENTER&gt;."
echo "Then, enter a second string (no \\ this time), and again press &lt;ENTER&gt;."

read var1     # The "\" suppresses the newline, when reading $var1.
              #     first line \
              #     second line

echo "var1 = $var1"
#     var1 = first line second line

#  For each line terminated by a "\"
#+ you get a prompt on the next line to continue feeding characters into var1.

echo; echo

echo "Enter another string terminated by a \\ , then press &lt;ENTER&gt;."
read -r var2  # The -r option causes the "\" to be read literally.
              #     first line \

echo "var2 = $var2"
#     var2 = first line \

# Data entry terminates with the first &lt;ENTER&gt;.

echo 

exit 0
