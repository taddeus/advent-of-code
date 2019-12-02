#!/usr/bin/env bash
python=${PYTHON:-python3}
trap exit SIGINT
for dir in "$@"; do
    i=1
    for f in $dir/[012]*.py
    do
        echo "-- dir $dir -- problem $i ----------------------------"
        cmd="`which time` -f 'elapsed: %E' $python $f"
        if [ -e $dir/input/$i ]
        then cmd+=" < $dir/input/$i"
        fi
        eval $cmd
        echo
        i=$((i + 1))
    done
done
