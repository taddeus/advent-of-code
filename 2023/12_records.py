#!/usr/bin/env python3
import sys
from functools import cache

@cache
def fit(size, record):
    remainders = []
    for start in range(1, len(record) - size):
        end = start + size
        if record[start - 1] != '#' and record[end] != '#' and \
                all(record[i] != '.' for i in range(start, end)):
            remainders.append('.' + record[end + 1:])
        if record[start] == '#':
            break
    return tuple(remainders)

@cache
def repair(record, sizes):
    if not sizes:
        return int('#' not in record)
    return sum(repair(r, sizes[1:]) for r in fit(sizes[0], record))

def normalize(record):
    return '.' + '.'.join(record.replace('.', ' ').split()) + '.'

records = [(record, tuple(map(int, numbers.split(','))))
           for record, numbers in map(str.split, sys.stdin)]
print(sum(repair(normalize(r), d) for r, d in records))
print(sum(repair(normalize('?'.join([r] * 5)), d * 5) for r, d in records))
