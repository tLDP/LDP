#!/bin/bash

username0=
# username0 has been declared, but is set to null.
echo "username0 = ${username0-`whoami`}"
# Will not echo.

echo "username1 = ${username1-`whoami`}"
# username1 has not been declared.
# Will echo.

username2=
# username2 has been declared, but is set to null.
echo "username2 = ${username2:-`whoami`}"
# Will echo because of :- rather than just - in condition test.

exit 0
