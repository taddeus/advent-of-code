#!/usr/bin/env python3
import sys
changes = list(map(int, sys.stdin))

print(sum(changes))

n = 0
seen = set([n])
twice = None
while twice is None:
    for i in changes:
        n += i
        if n in seen:
            twice = n
            break
        seen.add(n)
print(twice)
