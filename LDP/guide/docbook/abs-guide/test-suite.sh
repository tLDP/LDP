#!/bin/bash
# test-suite.sh
# A partial Bash compatibility test suite.
# Run this on your version of Bash, or some other shell.

default_option=FAIL         # Tests below will fail unless . . .

echo
echo -n "Testing "
sleep 1; echo -n ". "
sleep 1; echo -n ". "
sleep 1; echo ". "
echo

# Double brackets
String="Double brackets supported?"
echo -n "Double brackets test: "
if [[ "$String" = "Double brackets supported?" ]]
then
  echo "PASS"
else
  echo "FAIL"
fi


# Double brackets and regex matching
String="Regex matching supported?"
echo -n "Regex matching: "
if [[ "$String" =~ R.....matching* ]]
then
  echo "PASS"
else
  echo "FAIL"
fi


# Arrays
test_arr=$default_option     # FAIL
Array=( If supports arrays will print PASS )
test_arr=${Array[5]}
echo "Array test: $test_arr"


# Command Substitution
csub_test ()
{
  echo "PASS"
}

test_csub=$default_option    # FAIL
test_csub=$(csub_test)
echo "Command substitution test: $test_csub"

echo

#  Completing this script is an exercise for the reader.
#  Add to the above similar tests for double parentheses,
#+ brace expansion, process substitution, etc.

exit $?
