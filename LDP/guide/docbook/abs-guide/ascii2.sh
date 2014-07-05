#!/bin/bash
# Script author: Joseph Steinhauser
# Lightly edited by ABS Guide author, but not commented.
# Used in ABS Guide with permission.

#-------------------------------------------------------------------------
#-- File:  ascii.sh    Print ASCII chart, base 10/8/16         (JETS-2012)
#-------------------------------------------------------------------------
#-- Usage: ascii [oct|dec|hex|help|8|10|16]
#--
#-- This script prints out a summary of ASCII char codes from Zero to 127.
#-- Numeric values may be printed in Base10, Octal, or Hex.
#--
#-- Format Based on: /usr/share/lib/pub/ascii with base-10 as default.
#-- For more detail, man ascii . . .
#-------------------------------------------------------------------------

[ -n "$BASH_VERSION" ] &amp;&amp; shopt -s extglob

case "$1" in
   oct|[Oo]?([Cc][Tt])|8)       Obase=Octal;  Numy=3o;;
   hex|[Hh]?([Ee][Xx])|16|[Xx]) Obase=Hex;    Numy=2X;;
   help|?(-)[h?])        sed -n '2,/^[ ]*$/p' $0;exit;;
   code|[Cc][Oo][Dd][Ee])sed -n '/case/,$p'   $0;exit;;
   *) Obase=Decimal
esac # CODE is actually shorter than the chart!

printf "\t\t## $Obase ASCII Chart ##\n\n"; FM1="|%0${Numy:-3d}"; LD=-1

AB="nul soh stx etx eot enq ack bel bs tab nl vt np cr so si dle"
AD="dc1 dc2 dc3 dc4 nak syn etb can em sub esc fs gs rs us sp"

for TOK in $AB $AD; do ABR[$((LD+=1))]=$TOK; done;
ABR[127]=del

IDX=0
while [ $IDX -le 127 ] &amp;&amp; CHR="${ABR[$IDX]}"
   do ((${#CHR}))&amp;&amp; FM2='%-3s'|| FM2=`printf '\\\\%o  ' $IDX`
      printf "$FM1 $FM2" "$IDX" $CHR; (( (IDX+=1)%8))||echo '|'
   done

exit $?
