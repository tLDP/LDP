#!/bin/bash
# gronsfeld.bash

# License: GPL3
# Reldate 06/23/11

#  This is an implementation of the Gronsfeld Cipher.
#  It's essentially a stripped-down variant of the 
#+ polyalphabetic Vigen&egrave;re Tableau, but with only 10 alphabets.
#  The classic Gronsfeld has a numeric sequence as the key word,
#+ but here we substitute a letter string, for ease of use.
#  Allegedly, this cipher was invented by the eponymous Count Gronsfeld
#+ in the 17th Century. It was at one time considered to be unbreakable.
#  Note that this is ###not### a secure cipher by modern standards.

#  Global Variables  #
Enc_suffix="29379"   #  Encrypted text output with this 5-digit suffix. 
                     #  This functions as a decryption flag,
                     #+ and when used to generate passwords adds security.
Default_key="gronsfeldk"
                     #  The script uses this if key not entered below
                     #  (at "Keychain").
                     #  Change the above two values frequently
                     #+ for added security.

GROUPLEN=5           #  Output in groups of 5 letters, per tradition.
alpha1=( abcdefghijklmnopqrstuvwxyz )
alpha2=( {A..Z} )    #  Output in all caps, per tradition.
                     #  Use   alpha2=( {a..z} )   for password generator.
wraplen=26           #  Wrap around if past end of alphabet.
dflag=               #  Decrypt flag (set if $Enc_suffix present).
E_NOARGS=76          #  Missing command-line args?
DEBUG=77             #  Debugging flag.
declare -a offsets   #  This array holds the numeric shift values for
                     #+ encryption/decryption.

########Keychain#########
key=  ### Put key here!!!
      # 10 characters!
#########################



# Function
: ()
{ # Encrypt or decrypt, depending on whether $dflag is set.
  # Why ": ()" as a function name? Just to prove that it can be done.

  local idx keydx mlen off1 shft
  local plaintext="$1"
  local mlen=${#plaintext}

for (( idx=0; idx&lt;$mlen; idx++ ))
do
  let "keydx = $idx % $keylen"
  shft=${offsets[keydx]}

  if [ -n "$dflag" ]
  then                  # Decrypt!
    let "off1 = $(expr index "${alpha1[*]}" ${plaintext:idx:1}) - $shft"
    # Shift backward to decrypt.
  else                  # Encrypt!
    let "off1 = $(expr index "${alpha1[*]}" ${plaintext:idx:1}) + $shft"
    # Shift forward to encrypt.
    test $(( $idx % $GROUPLEN)) = 0 &amp;&amp; echo -n " "  # Groups of 5 letters.
    #  Comment out above line for output as a string without whitespace,
    #+ for example, if using the script as a password generator.
  fi

  ((off1--))   # Normalize. Why is this necessary?

      if [ $off1 -lt 0 ]
      then     # Catch negative indices.
        let "off1 += $wraplen"
      fi

  ((off1 %= $wraplen))   # Wrap around if past end of alphabet.

  echo -n "${alpha2[off1]}"

done

  if [ -z "$dflag" ]
  then
    echo " $Enc_suffix"
#   echo "$Enc_suffix"  # For password generator.
  else
    echo
  fi
} # End encrypt/decrypt function.



# int main () {

# Check for command-line args.
if [ -z "$1" ]
then
   echo "Usage: $0 TEXT TO ENCODE/DECODE"
   exit $E_NOARGS
fi

if [ ${!#} == "$Enc_suffix" ]
#    ^^^^^ Final command-line arg.
then
  dflag=ON
  echo -n "+"           # Flag decrypted text with a "+" for easy ID.
fi

if [ -z "$key" ]
then
  key="$Default_key"    # "gronsfeldk" per above.
fi

keylen=${#key}

for (( idx=0; idx&lt;$keylen; idx++ ))
do  # Calculate shift values for encryption/decryption.
  offsets[idx]=$(expr index "${alpha1[*]}" ${key:idx:1})   # Normalize.
  ((offsets[idx]--))  #  Necessary because "expr index" starts at 1,
                      #+ whereas array count starts at 0.
  # Generate array of numerical offsets corresponding to the key.
  # There are simpler ways to accomplish this.
done

args=$(echo "$*" | sed -e 's/ //g' | tr A-Z a-z | sed -e 's/[0-9]//g')
# Remove whitespace and digits from command-line args.
# Can modify to also remove punctuation characters, if desired.

         # Debug:
         # echo "$args"; exit $DEBUG

: "$args"               # Call the function named ":".
# : is a null operator, except . . . when it's a function name!

exit $?    # } End-of-script


#   **************************************************************   #
#   This script can function as a  password generator,
#+  with several minor mods, see above.
#   That would allow an easy-to-remember password, even the word
#+ "password" itself, which encrypts to vrgfotvo29379
#+  a fairly secure password not susceptible to a dictionary attack.
#   Or, you could use your own name (surely that's easy to remember!).
#   For example, Bozo Bozeman encrypts to hfnbttdppkt29379.
#   **************************************************************   #
