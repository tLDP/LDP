#!/bin/bash
# stack.sh: push-down stack simulation

#  Similar to the CPU stack, a push-down stack stores data items
#+ sequentially, but releases them in reverse order, last-in first-out.

BP=100            # Base Pointer of stack array.
                  # Begin at element 100.

SP=$BP            # Stack Pointer.
                  # Initialize it to "base" (bottom) of stack.

Data=             # Contents of stack location.  
                  #  Must use local variable,
                  #+ because of limitation on function return range.

declare -a stack


push()            # Push item on stack.
{
if [ -z "$1" ]    # Nothing to push?
then
  return
fi

let "SP -= 1"     # Bump stack pointer.
stack[$SP]=$1

return
}

pop()                    # Pop item off stack.
{
Data=                    # Empty out data item.

if [ "$SP" -eq "$BP" ]   # Stack empty?
then
  return
fi                       #  This also keeps SP from getting past 100,
                         #+ i.e., prevents a runaway stack.

Data=${stack[$SP]}
let "SP += 1"            # Bump stack pointer.
return
}

status_report()          # Find out what's happening.
{
echo "-------------------------------------"
echo "REPORT"
echo "Stack Pointer = $SP"
echo "Just popped \""$Data"\" off the stack."
echo "-------------------------------------"
echo
}


# =======================================================
# Now, for some fun.

echo

# See if you can pop anything off empty stack.
pop
status_report

echo

push garbage
pop
status_report     # Garbage in, garbage out.      

value1=23; push $value1
value2=skidoo; push $value2
value3=FINAL; push $value3

pop              # FINAL
status_report
pop              # skidoo
status_report
pop              # 23
status_report    # Last-in, first-out!

#  Notice how the stack pointer decrements with each push,
#+ and increments with each pop.

echo
# =======================================================


# Exercises:
# ---------

# 1)  Modify the "push()" function to permit pushing
#   + multiple element on the stack with a single function call.

# 2)  Modify the "pop()" function to permit popping
#   + multiple element from the stack with a single function call.

# 3)  Using this script as a jumping-off point,
#   + write a stack-based 4-function calculator.

exit 0
