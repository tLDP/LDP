#!/bin/bash

#  UseGetOpt-2.sh
#  Modified version of the script for illustrating tab-expansion
#+ of command-line options.
#  See the "Introduction to Tab Expansion" appendix.

#  Possible options: -a -d -f -l -t -h
#+                   --aoption, --debug --file --log --test -- help --

#  Author of original script: Peggy Russell &lt;prusselltechgroup@gmail.com&gt;


# UseGetOpt () {
  declare inputOptions
  declare -r E_OPTERR=85
  declare -r ScriptName=${0##*/}
  declare -r ShortOpts="adf:hlt"
  declare -r LongOpts="aoption,debug,file:,help,log,test"

DoSomething () {
    echo "The function name is '${FUNCNAME}'"
  }

  inputOptions=$(getopt -o "${ShortOpts}" --long \
              "${LongOpts}" --name "${ScriptName}" -- "${@}")

  if [[ ($? -ne 0) || ($# -eq 0) ]]; then
    echo "Usage: ${ScriptName} [-dhlt] {OPTION...}"
    exit $E_OPTERR
  fi

  eval set -- "${inputOptions}"


  while true; do
    case "${1}" in
      --aoption | -a)  # Argument found.
        echo "Option [$1]"
        ;;

      --debug | -d)    # Enable informational messages.
        echo "Option [$1] Debugging enabled"
        ;;

      --file | -f)     #  Check for optional argument.
        case "$2" in   #+ Double colon is optional argument.
          "")          #  Not there.
              echo "Option [$1] Use default"
              shift
              ;;

          *) # Got it
             echo "Option [$1] Using input [$2]"
             shift
             ;;

        esac
        DoSomething
        ;;

      --log | -l) # Enable Logging.
        echo "Option [$1] Logging enabled"
        ;;

      --test | -t) # Enable testing.
        echo "Option [$1] Testing enabled"
        ;;

      --help | -h)
        echo "Option [$1] Display help"
        break
        ;;

      --)   # Done! $# is argument number for "--", $@ is "--"
        echo "Option [$1] Dash Dash"
        break
        ;;

       *)
        echo "Major internal error!"
        exit 8
        ;;

    esac
    echo "Number of arguments: [$#]"
    shift
  done

  shift
  
#  }

exit
