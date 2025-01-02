#!/usr/bin/env python3
import sys

def parse(f):
    locks = []
    keys = []
    for group in f.read().split('\n\n'):
        lines = group.split()
        ident = tuple(col.count('#') - 1 for col in zip(*lines))
        (keys, locks)[lines[0] == '#####'].append(ident)
    return locks, keys

def fits(lock, key):
    return all(l + k <= 5 for l, k in zip(lock, key))

locks, keys = parse(sys.stdin)
print(sum(fits(lock, key) for lock in locks for key in keys))
