#!/usr/bin/env python3
import sys
from collections import Counter

def parse(f):
    yield next(f).rstrip()
    next(f)
    yield dict(line.rstrip().split(' -> ') for line in f)

def grow(polymer, rules, steps):
    elements = Counter(polymer)
    pairs = Counter(polymer[i:i + 2] for i in range(len(polymer) - 1))

    for step in range(steps):
        new = Counter()
        for pair, num in pairs.items():
            if pair in rules:
                a, b = pair
                c = rules[pair]
                new[a + c] += num
                new[c + b] += num
                elements[c] += num
            else:
                new[pair] = num
        pairs = new

    return max(elements.values()) - min(elements.values())

template, rules = parse(sys.stdin)
print(grow(template, rules, 10))
print(grow(template, rules, 40))
