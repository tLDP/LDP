#!/bin/bash

: ${HOSTNAME?} {USER?} {MAIL?}
  echo $HOSTNAME
  echo $USER
  echo $MAIL
  echo Critical env. variables set.

exit 0 
