#!/usr/bin/env python3
import sys

def scan(block_ranges, maxval):
    starts, ends = (sorted(l, reverse=True) for l in zip(*block_ranges))
    open_start = blocked = 0
    while starts:
        if starts[-1] <= ends[-1]:
            start = starts.pop()
            if blocked == 0 and start > 0 and open_start >= start - 1:
                yield open_start, start - 1
            blocked += 1
        else:
            end = ends.pop()
            blocked -= 1
            if blocked == 0 and end + 1 != starts[-1]:
                open_start = end + 1
    if ends[0] < maxval:
        yield ends[0] + 1, maxval

block_ranges = [tuple(map(int, line.split('-'))) for line in sys.stdin]
open_ranges = list(scan(block_ranges, 4294967295))
print(open_ranges[0][0])
print(sum(end - start + 1 for start, end in open_ranges))
