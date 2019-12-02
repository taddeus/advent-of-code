#!/usr/bin/env python3
import sys

def redistribute(banks):
    i = max(range(len(banks)), key=banks.__getitem__)
    blocks = banks[i]
    banks[i] = 0
    while blocks > 0:
        i = (i + 1) % len(banks)
        banks[i] += 1
        blocks -= 1

def cycle_iter_len(banks):
    seen = set()
    cycles = 0
    tup = tuple(banks)
    while tup not in seen:
        seen.add(tup)
        redistribute(banks)
        tup = tuple(banks)
        cycles += 1
    return cycles

banks = list(map(int, sys.stdin.readline().split()))
print(cycle_iter_len(banks))
print(cycle_iter_len(banks))
