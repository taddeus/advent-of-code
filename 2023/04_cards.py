#!/usr/bin/env python3
import sys

def matches(line):
    left, right = line.split(': ')[1].split(' | ')
    return len(set(left.split()) & set(right.split()))

def accumulate(cards):
    count = [1] * len(cards)
    for i, m in enumerate(cards):
        for j in range(i + 1, min(i + 1 + m, len(count))):
            count[j] += count[i]
    return sum(count)

cards = list(map(matches, sys.stdin))
print(sum(int(2 ** (m - 1)) for m in cards))
print(accumulate(cards))
