#!/usr/bin/env python3
import sys

def fuels(crabs, fuel):
    for dest in range(min(crabs), max(crabs) + 1):
        yield sum(fuel(abs(dest - crab)) for crab in crabs)

crabs = list(map(int, sys.stdin.readline().split(',')))
print(min(fuels(crabs, lambda dist: dist)))
print(min(fuels(crabs, lambda dist: dist * (dist + 1) // 2)))
