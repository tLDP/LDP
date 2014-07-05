#!/bin/bash
# sam.sh, v. .01a
# Still Another Morse (code training script)
# With profuse apologies to Sam (F.B.) Morse.
# Author: Mendel Cooper
# License: GPL3
# Reldate: 05/25/11

# Morse code training script.
# Converts arguments to audible dots and dashes.
# Note: lowercase input only at this time.



# Get the wav files from the source tarball:
# http://bash.deta.in/abs-guide-latest.tar.bz2
DOT='soundfiles/dot.wav'
DASH='soundfiles/dash.wav'
# Maybe move soundfiles to /usr/local/sounds?

LETTERSPACE=300000  # Microseconds.
WORDSPACE=980000
# Nice and slow, for beginners. Maybe 5 wpm?

EXIT_MSG="May the Morse be with you!"
E_NOARGS=75         # No command-line args?



declare -A morse    # Associative array!
# ======================================= #
morse[a]="dot; dash"
morse[b]="dash; dot; dot; dot"
morse[c]="dash; dot; dash; dot"
morse[d]="dash; dot; dot"
morse[e]="dot"
morse[f]="dot; dot; dash; dot"
morse[g]="dash; dash; dot"
morse[h]="dot; dot; dot; dot"
morse[i]="dot; dot;"
morse[j]="dot; dash; dash; dash"
morse[k]="dash; dot; dash"
morse[l]="dot; dash; dot; dot"
morse[m]="dash; dash"
morse[n]="dash; dot"
morse[o]="dash; dash; dash"
morse[p]="dot; dash; dash; dot"
morse[q]="dash; dash; dot; dash"
morse[r]="dot; dash; dot"
morse[s]="dot; dot; dot"
morse[t]="dash"
morse[u]="dot; dot; dash"
morse[v]="dot; dot; dot; dash"
morse[w]="dot; dash; dash"
morse[x]="dash; dot; dot; dash"
morse[y]="dash; dot; dash; dash"
morse[z]="dash; dash; dot; dot"
morse[0]="dash; dash; dash; dash; dash"
morse[1]="dot; dash; dash; dash; dash"
morse[2]="dot; dot; dash; dash; dash"
morse[3]="dot; dot; dot; dash; dash"
morse[4]="dot; dot; dot; dot; dash"
morse[5]="dot; dot; dot; dot; dot"
morse[6]="dash; dot; dot; dot; dot"
morse[7]="dash; dash; dot; dot; dot"
morse[8]="dash; dash; dash; dot; dot"
morse[9]="dash; dash; dash; dash; dot"
# The following must be escaped or quoted.
morse[?]="dot; dot; dash; dash; dot; dot"
morse[.]="dot; dash; dot; dash; dot; dash"
morse[,]="dash; dash; dot; dot; dash; dash"
morse[/]="dash; dot; dot; dash; dot"
morse[\@]="dot; dash; dash; dot; dash; dot"
# ======================================= #

play_letter ()
{
  eval ${morse[$1]}   # Play dots, dashes from appropriate sound files.
  # Why is 'eval' necessary here?
  usleep $LETTERSPACE # Pause in between letters.
}

extract_letters ()
{                     # Slice string apart, letter by letter.
  local pos=0         # Starting at left end of string.
  local len=1         # One letter at a time.
  strlen=${#1}

  while [ $pos -lt $strlen ]
  do
    letter=${1:pos:len}
    #      ^^^^^^^^^^^^    See Chapter 10.1.
    play_letter $letter
    echo -n "*"       #    Mark letter just played.
    ((pos++))
  done
}

######### Play the sounds ############
dot()  { aplay "$DOT" 2&amp;>/dev/null;  }
dash() { aplay "$DASH" 2&amp;>/dev/null; }
######################################

no_args ()
{
    declare -a usage
    usage=( $0 word1 word2 ... )

    echo "Usage:"; echo
    echo ${usage[*]}
    for index in 0 1 2 3
    do
      extract_letters ${usage[index]}     
      usleep $WORDSPACE
      echo -n " "     # Print space between words.
    done
#   echo "Usage: $0 word1 word2 ... "
    echo; echo
}


# int main()
# {

clear                 # Clear the terminal screen.
echo "            SAM"
echo "Still Another Morse code trainer"
echo "    Author: Mendel Cooper"
echo; echo;

if [ -z "$1" ]
then
  no_args
  echo; echo; echo "$EXIT_MSG"; echo
  exit $E_NOARGS
fi

echo; echo "$*"       # Print text that will be played.

until [ -z "$1" ]
do
  extract_letters $1
  shift           # On to next word.
  usleep $WORDSPACE
  echo -n " "     # Print space between words.
done

echo; echo; echo "$EXIT_MSG"; echo

exit 0
# }

#  Exercises:
#  ---------
#  1) Have the script accept either lowercase or uppercase words
#+    as arguments. Hint: Use 'tr' . . .
#  2) Have the script optionally accept input from a text file.
