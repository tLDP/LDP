#!/bin/bash
# base64.sh: Bash implementation of Base64 encoding and decoding.
#
# Copyright (c) 2011 vladz &lt;vladz@devzero.fr&gt;
# Used in ABSG with permission (thanks!).
#
#  Encode or decode original Base64 (and also Base64url)
#+ from STDIN to STDOUT.
#
#    Usage:
#
#    Encode
#    $ ./base64.sh &lt; binary-file > binary-file.base64
#    Decode
#    $ ./base64.sh -d &lt; binary-file.base64 > binary-file
#
# Reference:
#
#    [1]  RFC4648 - "The Base16, Base32, and Base64 Data Encodings"
#         http://tools.ietf.org/html/rfc4648#section-5


# The base64_charset[] array contains entire base64 charset,
# and additionally the character "=" ...
base64_charset=( {A..Z} {a..z} {0..9} + / = )
                # Nice illustration of brace expansion.

#  Uncomment the ### line below to use base64url encoding instead of
#+ original base64.
### base64_charset=( {A..Z} {a..z} {0..9} - _ = )

#  Output text width when encoding
#+ (64 characters, just like openssl output).
text_width=64

function display_base64_char {
#  Convert a 6-bit number (between 0 and 63) into its corresponding values
#+ in Base64, then display the result with the specified text width.
  printf "${base64_charset[$1]}"; (( width++ ))
  (( width % text_width == 0 )) &amp;&amp; printf "\n"
}

function encode_base64 {
# Encode three 8-bit hexadecimal codes into four 6-bit numbers.
  #    We need two local int array variables:
  #    c8[]: to store the codes of the 8-bit characters to encode
  #    c6[]: to store the corresponding encoded values on 6-bit
  declare -a -i c8 c6

  #  Convert hexadecimal to decimal.
  c8=( $(printf "ibase=16; ${1:0:2}\n${1:2:2}\n${1:4:2}\n" | bc) )

  #  Let's play with bitwise operators
  #+ (3x8-bit into 4x6-bits conversion).
  (( c6[0] = c8[0] >> 2 ))
  (( c6[1] = ((c8[0] &amp;  3) &lt;&lt; 4) | (c8[1] >> 4) ))

  # The following operations depend on the c8 element number.
  case ${#c8[*]} in 
    3) (( c6[2] = ((c8[1] &amp; 15) &lt;&lt; 2) | (c8[2] >> 6) ))
       (( c6[3] = c8[2] &amp; 63 )) ;;
    2) (( c6[2] = (c8[1] &amp; 15) &lt;&lt; 2 ))
       (( c6[3] = 64 )) ;;
    1) (( c6[2] = c6[3] = 64 )) ;;
  esac

  for char in ${c6[@]}; do
    display_base64_char ${char}
  done
}

function decode_base64 {
# Decode four base64 characters into three hexadecimal ASCII characters.
  #  c8[]: to store the codes of the 8-bit characters
  #  c6[]: to store the corresponding Base64 values on 6-bit
  declare -a -i c8 c6

  # Find decimal value corresponding to the current base64 character.
  for current_char in ${1:0:1} ${1:1:1} ${1:2:1} ${1:3:1}; do
     [ "${current_char}" = "=" ] &amp;&amp; break

     position=0
     while [ "${current_char}" != "${base64_charset[${position}]}" ]; do
        (( position++ ))
     done

     c6=( ${c6[*]} ${position} )
  done

  #  Let's play with bitwise operators
  #+ (4x8-bit into 3x6-bits conversion).
  (( c8[0] = (c6[0] &lt;&lt; 2) | (c6[1] >> 4) ))

  # The next operations depends on the c6 elements number.
  case ${#c6[*]} in
    3) (( c8[1] = ( (c6[1] &amp; 15) &lt;&lt; 4) | (c6[2] >> 2) ))
       (( c8[2] = (c6[2] &amp; 3) &lt;&lt; 6 )); unset c8[2] ;;
    4) (( c8[1] = ( (c6[1] &amp; 15) &lt;&lt; 4) | (c6[2] >> 2) ))
       (( c8[2] = ( (c6[2] &amp;  3) &lt;&lt; 6) |  c6[3] )) ;;
  esac

  for char in ${c8[*]}; do
     printf "\x$(printf "%x" ${char})"
  done
}


# main ()

if [ "$1" = "-d" ]; then   # decode

  # Reformat STDIN in pseudo 4x6-bit groups.
  content=$(cat - | tr -d "\n" | sed -r "s/(.{4})/\1 /g")

  for chars in ${content}; do decode_base64 ${chars}; done

else
  # Make a hexdump of stdin and reformat in 3-byte groups.
  content=$(cat - | xxd -ps -u | sed -r "s/(\w{6})/\1 /g" |
            tr -d "\n")

  for chars in ${content}; do encode_base64 ${chars}; done

  echo

fi
