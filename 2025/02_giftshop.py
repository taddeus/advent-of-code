#!/usr/bin/env python3
import sys

def expand(inp):
    for range_str in inp.read().rstrip().split(','):
        l, r = range_str.split('-')
        yield from range(int(l), int(r) + 1)

def repetitions(num):
    text = str(num)
    for reps in range(2, len(text) + 1):
        n, rem = divmod(len(text), reps)
        if rem == 0:
            batches = set(text[i:i + n] for i in range(0, len(text), n))
            if len(batches) == 1:
                return reps

def filter_repeating(ids):
    for i in ids:
        reps = repetitions(i)
        if reps:
            yield i, reps

reps = list(filter_repeating(expand(sys.stdin)))
print(sum(i for i, reps in reps if reps == 2))
print(sum(i for i, _ in reps))
