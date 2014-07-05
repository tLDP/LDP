#!/bin/bash
#  assoc-arr-test.sh
#  Benchmark test script to compare execution times of
#  numeric-indexed array vs. associative array.
#     Thank you, Erik Brandsberg.

count=100000       # May take a while for some of the tests below.
declare simple     # Can change to 20000, if desired.
declare -a array1
declare -A array2
declare -a array3
declare -A array4

echo "===Assignment tests==="
echo

echo "Assigning a simple variable:"
# References $i twice to equalize lookup times.
time for (( i=0; i&lt; $count; i++)); do
        simple=$i$i
done

echo "---"

echo "Assigning a numeric index array entry:"
time for (( i=0; i&lt; $count; i++)); do
        array1[$i]=$i
done

echo "---"

echo "Overwriting a numeric index array entry:"
time for (( i=0; i&lt; $count; i++)); do
        array1[$i]=$i
done

echo "---"

echo "Linear reading of numeric index array:"
time for (( i=0; i&lt; $count; i++)); do
        simple=array1[$i]
done

echo "---"

echo "Assigning an associative array entry:"
time for (( i=0; i&lt; $count; i++)); do
        array2[$i]=$i
done

echo "---"

echo "Overwriting an associative array entry:"
time for (( i=0; i&lt; $count; i++)); do
        array2[$i]=$i
done

echo "---"

echo "Linear reading an associative array entry:"
time for (( i=0; i&lt; $count; i++)); do
        simple=array2[$i]
done

echo "---"

echo "Assigning a random number to a simple variable:"
time for (( i=0; i&lt; $count; i++)); do
        simple=$RANDOM
done

echo "---"

echo "Assign a sparse numeric index array entry randomly into 64k cells:"
time for (( i=0; i&lt; $count; i++)); do
        array3[$RANDOM]=$i
done

echo "---"

echo "Reading sparse numeric index array entry:"
time for value in "${array3[@]}"i; do
        simple=$value
done

echo "---"

echo "Assigning a sparse associative array entry randomly into 64k cells:"
time for (( i=0; i&lt; $count; i++)); do
        array4[$RANDOM]=$i
done

echo "---"

echo "Reading sparse associative index array entry:"
time for value in "${array4[@]}"; do
        simple=$value
done

exit $?
