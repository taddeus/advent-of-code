#!/usr/bin/env bash
python=${PYTHON:-python3}
trap exit SIGINT
for year in "$@"; do
    day=1
    for solution in $year/[012]*.py do
        echo "-- year $year -- day $day -------------------------------"
        [ -e $year/input/$day ] && inp=$year/input/$day || inp=/dev/null
        `which time` -f 'elapsed: %E' "$python" $solution < $inp
        echo
        day=$((day + 1))
    done
done
