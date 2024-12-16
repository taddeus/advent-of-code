#!/usr/bin/env python3
import sys
from collections import Counter

def change(stone):
    if stone == 0:
        yield 1
    else:
        digits = str(stone)
        mid, odd = divmod(len(digits), 2)
        if odd:
            yield stone * 2024
        else:
            yield int(digits[:mid])
            yield int(digits[mid:])

def blink(counts, times):
    for _ in range(times):
        new = Counter()
        for stone, occurrences in counts.items():
            for newstone in change(stone):
                new[newstone] += occurrences
        counts = new
    return counts

counts = Counter(map(int, next(sys.stdin).split()))
counts = blink(counts, 25)
print(sum(counts.values()))
counts = blink(counts, 50)
print(sum(counts.values()))
