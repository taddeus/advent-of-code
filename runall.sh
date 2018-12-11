#!/bin/bash
i=1
for f in *.py
do
    echo "-- problem $i -----------------------------------"
    cmd="`which time` -f 'elapsed: %E' ./$f"
    if [ -e input/$i ]
    then cmd+=" < input/$i"
    fi
    eval $cmd
    echo
    i=$((i + 1))
done
