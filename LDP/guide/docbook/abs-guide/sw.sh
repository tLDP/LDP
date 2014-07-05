#!/bin/sh
# sw.sh
# A command-line Stopwatch

# Author: P&aacute;draig Brady
#    http://www.pixelbeat.org/scripts/sw
#    (Minor reformatting by ABS Guide author.)
#    Used in ABS Guide with script author's permission.
# Notes:
#    This script starts a few processes per lap, in addition to
#    the shell loop processing, so the assumption is made that
#    this takes an insignificant amount of time compared to
#    the response time of humans (~.1s) (or the keyboard
#    interrupt rate (~.05s)).
#    '?' for splits must be entered twice if characters
#    (erroneously) entered before it (on the same line).
#    '?' since not generating a signal may be slightly delayed
#    on heavily loaded systems.
#    Lap timings on ubuntu may be slightly delayed due to:
#    https://bugs.launchpad.net/bugs/62511
# Changes:
#    V1.0, 23 Aug 2005, Initial release
#    V1.1, 26 Jul 2007, Allow both splits and laps from single invocation.
#                       Only start timer after a key is pressed.
#                       Indicate lap number
#                       Cache programs at startup so there is less error
#                       due to startup delays.
#    V1.2, 01 Aug 2007, Work around `date` commands that don't have
#                       nanoseconds.
#                       Use stty to change interrupt keys to space for
#                       laps etc.
#                       Ignore other input as it causes problems.
#    V1.3, 01 Aug 2007, Testing release.
#    V1.4, 02 Aug 2007, Various tweaks to get working under ubuntu
#                       and Mac OS X.
#    V1.5, 27 Jun 2008, set LANG=C as got vague bug report about it.

export LANG=C

ulimit -c 0   # No coredumps from SIGQUIT.
trap '' TSTP  # Ignore Ctrl-Z just in case.
save_tty=`stty -g` &amp;&amp; trap "stty $save_tty" EXIT  # Restore tty on exit.
stty quit ' ' # Space for laps rather than Ctrl-\.
stty eof  '?' # ? for splits rather than Ctrl-D.
stty -echo    # Don't echo input.

cache_progs() {
    stty > /dev/null
    date > /dev/null
    grep . &lt; /dev/null
    (echo "import time" | python) 2> /dev/null
    bc &lt; /dev/null
    sed '' &lt; /dev/null
    printf '1' > /dev/null
    /usr/bin/time false 2> /dev/null
    cat &lt; /dev/null
}
cache_progs   # To minimise startup delay.

date +%s.%N | grep -qF 'N' &amp;&amp; use_python=1 # If `date` lacks nanoseconds.
now() {
    if [ "$use_python" ]; then
        echo "import time; print time.time()" 2>/dev/null | python
    else
        printf "%.2f" `date +%s.%N`
    fi
}

fmt_seconds() {
    seconds=$1
    mins=`echo $seconds/60 | bc`
    if [ "$mins" != "0" ]; then
        seconds=`echo "$seconds - ($mins*60)" | bc`
        echo "$mins:$seconds"
    else
        echo "$seconds"
    fi
}

total() {
    end=`now`
    total=`echo "$end - $start" | bc`
    fmt_seconds $total
}

stop() {
    [ "$lapped" ] &amp;&amp; lap "$laptime" "display"
    total
    exit
}

lap() {
    laptime=`echo "$1" | sed -n 's/.*real[^0-9.]*\(.*\)/\1/p'`
    [ ! "$laptime" -o "$laptime" = "0.00" ] &amp;&amp; return
    # Signals too frequent.
    laptotal=`echo $laptime+0$laptotal | bc`
    if [ "$2" = "display" ]; then
        lapcount=`echo 0$lapcount+1 | bc`
        laptime=`fmt_seconds $laptotal`
        echo $laptime "($lapcount)"
        lapped="true"
        laptotal="0"
    fi
}

echo -n "Space for lap | ? for split | Ctrl-C to stop | Space to start...">&amp;2

while true; do
    trap true INT QUIT  # Set signal handlers.
    laptime=`/usr/bin/time -p 2>&amp;1 cat >/dev/null`
    ret=$?
    trap '' INT QUIT    # Ignore signals within this script.
    if [ $ret -eq 1 -o $ret -eq 2 -o $ret -eq 130 ]; then # SIGINT = stop
        [ ! "$start" ] &amp;&amp; { echo >&amp;2; exit; }
        stop
    elif [ $ret -eq 3 -o $ret -eq 131 ]; then             # SIGQUIT = lap
        if [ ! "$start" ]; then
            start=`now` || exit 1
            echo >&amp;2
            continue
        fi
        lap "$laptime" "display"
    else                # eof = split
        [ ! "$start" ] &amp;&amp; continue
        total
        lap "$laptime"  # Update laptotal.
    fi
done

exit $?
