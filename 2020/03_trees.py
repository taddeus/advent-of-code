#!/usr/bin/env python3
import sys
from functools import reduce
from operator import mul

def count(treemap, right, down):
    return sum(line[((i + 1) * right) % len(line)]
               for i, line in enumerate(treemap[down::down]))

treemap = [[x == '#' for x in line.rstrip()] for line in sys.stdin]
print(count(treemap, 3, 1))
print(reduce(mul, (count(treemap, r, d)
                   for r, d, in ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2)))))
