#!/usr/bin/env python3
import sys
from functools import cache

@cache
def possible(design, towels):
    if not design:
        return 1
    return sum(possible(design[len(towel):], towels)
               for towel in towels if design.startswith(towel))

towels = tuple(sys.stdin.readline().rstrip().split(', '))
designs = sys.stdin.read().split()
pos = [possible(design, towels) for design in designs]
print(sum(map(bool, pos)))
print(sum(pos))
