#!/usr/bin/env python3
import sys
from collections import Counter

def change(stone):
    if stone == 0:
        yield 1
    else:
        s = str(stone)
        l = len(s)
        if l % 2 == 0:
            yield int(s[:l // 2])
            yield int(s[l // 2:])
        else:
            yield stone * 2024

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
