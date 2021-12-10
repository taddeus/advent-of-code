#!/usr/bin/env python3
import sys
from statistics import median

CLOSE = {'(': ')', '[': ']', '{': '}', '<': '>'}
CORRUPT = {')': 3, ']': 57, '}': 1197, '>': 25137}

def complete(chunk):
    expect = []
    for char in chunk:
        if char in CLOSE:
            expect.append(CLOSE[char])
        elif char != expect.pop():
            return -CORRUPT[char]

    score = 0
    for char in reversed(expect):
        score = score * 5 + ' )]}>'.index(char)
    return score

scores = [complete(line.rstrip()) for line in sys.stdin]
print(sum(-score for score in scores if score < 0))
print(median(score for score in scores if score > 0))
