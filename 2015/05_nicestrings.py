#!/usr/bin/env python3
import sys

def nice1(s):
    if sum(1 for c in s if c in 'aeiou') < 3:
        return False
    double = False
    for i in range(len(s) - 1):
        a, b = duo = s[i:i + 2]
        double |= a == b
        if duo in ('ab', 'cd', 'pq', 'xy'):
            return False
    return double

def nice2(s):
    prev = {}
    for i in range(len(s) - 1):
        pair = s[i:i + 2]
        if pair not in prev:
            prev[pair] = i
        elif prev[pair] < i - 1:
            break
    else:
        return False

    prev = {}
    for i, c in enumerate(s):
        if prev.get(c, None) == i - 2:
            return True
        prev[c] = i

    return False

strings = [line.rstrip() for line in sys.stdin]
print(sum(int(nice1(s)) for s in strings))
print(sum(int(nice2(s)) for s in strings))
