#!/usr/bin/env python3
import sys
from itertools import chain, islice

def possible(a, b, c):
    return a + b > c and b + c > a and a + c > b

triangles = [tuple(map(int, line.split())) for line in sys.stdin]
print(sum(int(possible(*t)) for t in triangles))

cols = chain.from_iterable(zip(*triangles))
coltris = (tuple(islice(cols, 3)) for i in range(len(triangles)))
print(sum(int(possible(*t)) for t in coltris))
