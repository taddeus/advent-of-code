#!/usr/bin/env python3
import sys
from functools import cache

def place_iter(size, record):
    groupend = record.find('.', 1) + 1
    if groupend != len(record):
        group = record[:groupend]
        for rem in place(size, group):
            yield rem + record[groupend:]
        if '#' not in group:
            yield from place(size, record[groupend - 1:])
    else:
        for start in range(1, len(record) - size):
            end = start + size
            if record[start - 1] != '#' and record[end] != '#' and \
                    all(record[i] != '.' for i in range(start, end)):
                yield '.' + record[min(end + 1, len(record) - 1):]
            if record[start] == '#':
                break

@cache
def place(size, record):
    return tuple(place_iter(size, record))

@cache
def arrangements(record, sizes):
    if not sizes:
        return int('#' not in record)
    return sum(arrangements(r, sizes[1:]) for r in place(sizes[0], record))

def normalize(record):
    return '.' + '.'.join(record.replace('.', ' ').split()) + '.'

records = [(record, tuple(map(int, numbers.split(','))))
           for record, numbers in map(str.split, sys.stdin)]
print(sum(arrangements(normalize(r), d) for r, d in records))
print(sum(arrangements(normalize('?'.join([r] * 5)), d * 5) for r, d in records))
