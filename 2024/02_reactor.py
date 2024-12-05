#!/usr/bin/env python3
import sys
from itertools import compress, pairwise

def safe_inc(report):
    return all(b - 3 <= a < b for a, b in pairwise(report))

def safe(report):
    return safe_inc(report) or safe_inc(reversed(report))

def masks(size):
    mask = [1] * size
    for i in range(size):
        mask[i - 1] = 1
        mask[i] = 0
        yield mask

def safe_dampened(report):
    return safe(report) or any(safe(list(compress(report, mask)))
                               for mask in masks(len(report)))

reports = [list(map(int, line.split())) for line in sys.stdin]
print(sum(map(safe, reports)))
print(sum(map(safe_dampened, reports)))
