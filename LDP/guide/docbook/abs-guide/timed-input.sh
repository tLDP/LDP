#!/bin/bash
# timed-input.sh

# TMOUT=3            useless in a script

TIMELIMIT=3  # Three seconds in this instance, may be set to different value.

PrintAnswer()
{
  if [ "$answer" = TIMEOUT ]
  then
    echo $answer
  else       # Don't want to mix up the two instances. 
    echo "Your favorite veggie is $answer"
    kill $!  # Kills no longer needed TimerOn function running in background.
             # $! is PID of last job running in background.
  fi

}  



TimerOn()
{
  sleep $TIMELIMIT && kill -s 14 $$ &
  # Waits 3 seconds, then sends sigalarm to script.
}  

Int14Vector()
{
  answer="TIMEOUT"
  PrintAnswer
  exit 14
}  

trap Int14Vector 14   # Timer interrupt (14) subverted for our purposes.

echo "What is your favorite vegetable "
TimerOn
read answer
PrintAnswer


#  Admittedly, this is a kludgy implementation of timed input,
#+ however the "-t" option to "read" simplifies this task.
#  See "t-out.sh", below.

#  If you need something really elegant...
#+ consider writing the application in C or C++,
#+ using appropriate library functions, such as 'alarm' and 'setitimer'.

exit 0
