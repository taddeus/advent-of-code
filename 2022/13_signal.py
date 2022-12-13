#!/usr/bin/env python3
import sys
from functools import cmp_to_key

def compare(l, r):
    if isinstance(l, int) and isinstance(r, int):
        return (l > r) - (l < r)

    if not isinstance(l, list): l = [l]
    elif not isinstance(r, list): r = [r]

    for a, b in zip(l, r):
        c = compare(a, b)
        if c != 0:
            return c

    return compare(len(l), len(r))

packets = [eval(line) for line in sys.stdin if line != '\n']
pairs = zip(packets[::2], packets[1::2])
print(sum(i + 1 for i, (a, b) in enumerate(pairs) if compare(a, b) == -1))

packets.extend(([[2]], [[6]], 0))
packets.sort(key=cmp_to_key(compare))
print(packets.index([[2]]) * packets.index([[6]]))
