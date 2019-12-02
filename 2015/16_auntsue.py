#!/usr/bin/env python3
import sys
from operator import eq, gt, lt

fields = ['children', 'cats', 'samoyeds', 'pomeranians', 'akitas',
          'vizslas', 'goldfish', 'trees', 'cars', 'perfumes']

def parse(f):
    for line in f:
        left, right = line.rstrip().split(': ', 1)
        sig = [None] * len(fields)
        for prop in right.split(', '):
            key, val = prop.split(': ')
            sig[fields.index(key)] = int(val)
        yield int(left[4:]), sig

def find_sue(needle, haystack):
    for sue, sig in haystack:
        if all(s is None or op(s, n) for s, (op, n) in zip(sig, needle)):
            return sue

sues = list(parse(sys.stdin))
sig = [(eq, n) for n in [3, 7, 2, 3, 0, 0, 5, 3, 2, 1]]
print(find_sue(sig, sues))

sig[1] = gt, 7
sig[7] = gt, 3
sig[3] = lt, 3
sig[6] = lt, 5
print(find_sue(sig, sues))
