#!/bin/bash
# multiple-processes.sh: Run multiple processes on an SMP box.

# Script written by Vernia Damiano.
# Used with permission.

#  Must call script with at least one integer parameter
#+ (number of concurrent processes).
#  All other parameters are passed through to the processes started.


INDICE=8        # Total number of process to start
TEMPO=5         # Maximum sleep time per process
E_BADARGS=65    # No arg(s) passed to script.

if [ $# -eq 0 ] # Check for at least one argument passed to script.
then
  echo "Usage: `basename $0` number_of_processes [passed params]"
  exit $E_BADARGS
fi

NUMPROC=$1              # Number of concurrent process
shift
PARAMETRI=( "$@" )      # Parameters of each process

function avvia() {
	local temp
	local index
	temp=$RANDOM
	index=$1
	shift
	let "temp %= $TEMPO"
	let "temp += 1"
	echo "Starting $index Time:$temp" "$@"
	sleep ${temp}
	echo "Ending $index"
	kill -s SIGRTMIN $$
}

function parti() {
	if [ $INDICE -gt 0 ] ; then
		avvia $INDICE "${PARAMETRI[@]}" &
		let "INDICE--"
	else
		trap : SIGRTMIN
	fi
}

trap parti SIGRTMIN

while [ "$NUMPROC" -gt 0 ]; do
	parti;
	let "NUMPROC--"
done

wait
trap - SIGRTMIN

exit $?

: &lt;&lt;SCRIPT_AUTHOR_COMMENTS
I had the need to run a program, with specified options, on a number of
different files, using a SMP machine. So I thought [I'd] keep running
a specified number of processes and start a new one each time . . . one
of these terminates.

The "wait" instruction does not help, since it waits for a given process
or *all* process started in background. So I wrote [this] bash script
that can do the job, using the "trap" instruction.
  --Vernia Damiano
SCRIPT_AUTHOR_COMMENTS
