#!/bin/bash
# match-string.sh: simple string matching

match_string ()
{
  MATCH=0
  NOMATCH=90
  PARAMS=2     # Function requires 2 arguments.
  BAD_PARAMS=91

  [ $# -eq $PARAMS ] || return $BAD_PARAMS

  case "$1" in
  "$2") return $MATCH;;
  *   ) return $NOMATCH;;
  esac

}  


a=one
b=two
c=three
d=two


match_string $a     # wrong number of parameters
echo $?             # 91

match_string $a $b  # no match
echo $?             # 90

match_string $b $d  # match
echo $?             # 0


exit 0		    
