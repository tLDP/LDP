#!/bin/bash4
# fetch_address-2.sh
# A more elaborate version of fetch_address.sh.

SUCCESS=0
E_DB=99    # Error code for missing entry.

declare -A address
#       -A option declares associative array.


store_address ()
{
  address[$1]="$2"
  return $?
}


fetch_address ()
{
  if [[ -z "${address[$1]}" ]]
  then
    echo "$1's address is not in database."
    return $E_DB
  fi

  echo "$1's address is ${address[$1]}."
  return $?
}


store_address "Charles Jones" "414 W. 10th Ave., Baltimore, MD 21236"
store_address "John Smith" "202 E. 3rd St., New York, NY 10009"
store_address "Wilma Wilson" "1854 Vermont Ave, Los Angeles, CA 90023"
#  Exercise:
#  Rewrite the above store_address calls to read data from a file,
#+ then assign field 1 to name, field 2 to address in the array.
#  Each line in the file would have a format corresponding to the above.
#  Use a while-read loop to read from file, sed or awk to parse the fields.

fetch_address "Charles Jones"
# Charles Jones's address is 414 W. 10th Ave., Baltimore, MD 21236.
fetch_address "Wilma Wilson"
# Wilma Wilson's address is 1854 Vermont Ave, Los Angeles, CA 90023.
fetch_address "John Smith"
# John Smith's address is 202 E. 3rd St., New York, NY 10009.
fetch_address "Bozo Bozeman"
# Bozo Bozeman's address is not in database.

exit $?   # In this case, exit code = 99, since that is function return.
