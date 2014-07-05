#!/bin/bash
#  test-execution-time.sh
#  Example by Erik Brandsberg, for testing execution time
#+ of certain operations.
#  Referenced in the "Optimizations" section of "Miscellany" chapter.

count=50000
echo "Math tests"
echo "Math via \$(( ))"
time for (( i=0; i&lt; $count; i++))
do
  result=$(( $i%2 ))
done

echo "Math via *expr*:"
time for (( i=0; i&lt; $count; i++))
do
  result=`expr "$i%2"`
done

echo "Math via *let*:"
time for (( i=0; i&lt; $count; i++))
do
  let result=$i%2
done

echo
echo "Conditional testing tests"

echo "Test via case:"
time for (( i=0; i&lt; $count; i++))
do
  case $(( $i%2 )) in
    0) : ;;
    1) : ;;
  esac
done

echo "Test with if [], no quotes:"
time for (( i=0; i&lt; $count; i++))
do
  if [ $(( $i%2 )) = 0 ]; then
     :
  else
     :
  fi
done

echo "Test with if [], quotes:"
time for (( i=0; i&lt; $count; i++))
do
  if [ "$(( $i%2 ))" = "0" ]; then
     :
  else
     :
  fi
done

echo "Test with if [], using -eq:"
time for (( i=0; i&lt; $count; i++))
do
  if [ $(( $i%2 )) -eq 0 ]; then
     :
  else
     :
  fi
done

exit $?
