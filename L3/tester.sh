#!/bin/bash
FILES="
tadek.txt"

CODES="-g
-d
-f"

total=0
passed=0

for f in $FILES
do
    for c in $CODES
    do
        echo -e "\nTESTING: $f"
        python lzw.py -E $f encoded $c
        python lzw.py -D encoded decoded $c
        fileSum=$(shasum -a 512 $f | cut -c1-128) 
        outSum=$(shasum -a 512 decoded | cut -c1-128) 
        if [ "$fileSum" = "$outSum" ]; then
            echo "TEST PASSED"
            ((passed++))
        else
            echo "TEST FAILED"
        fi
        ((total++))
    done
done

echo -e "\nPASSED: $passed/$total"