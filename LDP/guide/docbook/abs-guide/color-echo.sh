#!/bin/bash
# color-echo.sh: Echoing text messages in color.

# Modify this script for your own purposes.
# It's easier than hand-coding color.

black='\E[30;47m'
red='\E[31;47m'
green='\E[32;47m'
yellow='\E[33;47m'
blue='\E[34;47m'
magenta='\E[35;47m'
cyan='\E[36;47m'
white='\E[37;47m'


alias Reset="tput sgr0"      #  Reset text attributes to normal
                             #+ without clearing screen.


cecho ()                     # Color-echo.
                             # Argument $1 = message
                             # Argument $2 = color
{
local default_msg="No message passed."
                             # Doesn't really need to be a local variable.

message=${1:-$default_msg}   # Defaults to default message.
color=${2:-$black}           # Defaults to black, if not specified.

  echo -e "$color"
  echo "$message"
  Reset                      # Reset to normal.

  return
}  


# Now, let's try it out.
# ----------------------------------------------------
cecho "Feeling blue..." $blue
cecho "Magenta looks more like purple." $magenta
cecho "Green with envy." $green
cecho "Seeing red?" $red
cecho "Cyan, more familiarly known as aqua." $cyan
cecho "No color passed (defaults to black)."
       # Missing $color argument.
cecho "\"Empty\" color passed (defaults to black)." ""
       # Empty $color argument.
cecho
       # Missing $message and $color arguments.
cecho "" ""
       # Empty $message and $color arguments.
# ----------------------------------------------------

echo

exit 0

# Exercises:
# ---------
# 1) Add the "bold" attribute to the 'cecho ()' function.
# 2) Add options for colored backgrounds.
