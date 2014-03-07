#!/bin/bash
#   Courtesy of:
#   http://elinux.org/RPi_Text_to_Speech_(Speech_Synthesis)

#  You must be on-line for this script to work,
#+ so you can access the Google translation server.
#  Of course, mplayer must be present on your computer.

speak()
  {
  local IFS=+
  # Invoke mplayer, then connect to Google translation server.
  /usr/bin/mplayer -ao alsa -really-quiet -noconsolecontrols \
 "http://translate.google.com/translate_tts?tl=en&amp;q="$*""
  # Google translates, but can also speak.
  }

LINES=4

spk=$(tail -$LINES $0) # Tail end of same script!
speak "$spk"
exit
# Browns. Nice talking to you.
