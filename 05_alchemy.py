#!/usr/bin/env python3
import sys

def react(polymer):
    i = 0
    while i < len(polymer) - 1:
        if abs(polymer[i] - polymer[i + 1]) == 32:
            del polymer[i:i + 2]
            if i > 0:
                i -= 1
        else:
            i += 1
    return len(polymer)

def remove(polymer, ty):
    p = [c for c in polymer if c not in (ty, ty + 32)]
    return react(p) if len(p) < len(polymer) else len(p)

polymer = list(map(ord, sys.stdin.read().rstrip()))
print(react(polymer.copy()))
print(min(remove(polymer, ty) for ty in range(ord('A'), ord('Z'))))
