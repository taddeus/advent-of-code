#!/usr/bin/env python3
import sys

def reflect(pat, multiplier=100):
    for mirror in range(len(pat) - 1):
        if all(pat[mirror - dist] == pat[mirror + dist + 1]
               for dist in range(min(mirror + 1, len(pat) - mirror - 1))):
            yield multiplier * (mirror + 1)
    if multiplier == 100:
        yield from reflect(list(map(''.join, zip(*pat))), 1)

def fix_and_reflect(pat, old_reflection):
    for y, row in enumerate(pat):
        for x, smudge in enumerate(row):
            newrow = row[:x] + '#.'[smudge == '#'] + row[x + 1:]
            newpat = pat[:y] + [newrow] + pat[y + 1:]
            for reflection in reflect(newpat):
                if reflection != old_reflection:
                    return reflection

patterns = [pat.split() for pat in sys.stdin.read().split('\n\n')]
reflections = [next(reflect(pat)) for pat in patterns]
print(sum(reflections))
print(sum(fix_and_reflect(*p) for p in zip(patterns, reflections)))
