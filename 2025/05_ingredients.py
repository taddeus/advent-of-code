#!/usr/bin/env python3
import sys

def parse_ranges(f):
    for line in f:
        if line == '\n':
            break
        yield tuple(map(int, line.split('-')))

def merge(ranges):
    sorted_ranges = sorted(ranges)
    merged = [sorted_ranges[0]]
    for start, end in sorted_ranges[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end:
            merged[-1] = last_start, max(last_end, end)
        else:
            merged.append((start, end))
    return merged

def any_contains(ranges, number):
    return any(start <= number <= end for start, end in ranges)

fresh = merge(parse_ranges(sys.stdin))
inventory = map(int, sys.stdin)
print(sum(any_contains(fresh, ingredient) for ingredient in inventory))
print(sum(end - start + 1 for start, end in fresh))
