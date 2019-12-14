#!/usr/bin/env python3
import sys

def count_safe(first, nrows):
    row = [False] + [c == '^' for c in first] + [False]
    safe = len(row) - sum(row) - 2
    for step in range(nrows - 1):
        row[1:-1] = (row[i - 1] != row[i + 1] for i in range(1, len(row) - 1))
        safe += len(row) - sum(row) - 2
    return safe

first = sys.stdin.readline().rstrip()
print(count_safe(first, 40))
print(count_safe(first, 400000))
