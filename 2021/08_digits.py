#!/usr/bin/env python3
import sys

DIGITS = ('abcefg', 'cf', 'acdeg', 'acdfg', 'bcdf', 'abdfg', 'abdefg', 'acf',
          'abcdefg', 'abcdfg')
OVERLAPS = (None, None, 'cf', 'acf', 'bcdf', 'adg', 'abfg', 'abcdefg')

def parse(line):
    inputs, outputs = line.split(' | ')
    return inputs.split(), outputs.split()

def output(inp, outp):
    candidates = {c: set('abcdefg') for c in 'abcdefg'}
    for pattern in inp:
        for char in OVERLAPS[len(pattern)]:
            candidates[char] &= set(pattern)

    known = {}
    while any(candidates.values()):
        all_known = set(known.values())
        for char, possibilities in candidates.items():
            possibilities -= all_known
            if len(possibilities) == 1:
                known[char] = possibilities.pop()

    trans = str.maketrans(''.join(known[c] for c in 'abcdefg'), 'abcdefg')
    out = 0
    for pattern in outp:
        out = out * 10 + DIGITS.index(''.join(sorted(pattern.translate(trans))))
    return out

notes = list(map(parse, sys.stdin))
print(sum(sum(len(o) in (2, 3, 4, 7) for o in outp) for inp, outp in notes))
print(sum(output(i, o) for i, o in notes))
