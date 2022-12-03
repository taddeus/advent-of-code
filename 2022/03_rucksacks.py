#!/usr/bin/env python3
import sys

def prio(item):
    return (ord(item) - ord('a') + 1) % 58

def split(pack):
    return pack[:len(pack) // 2], pack[len(pack) // 2:]

def group(packs):
    cur = []
    for pack in packs:
        cur.append(pack)
        if len(cur) == 3:
            yield cur
            cur = []

packs = [line.rstrip() for line in sys.stdin]
print(sum(prio(next(i for i in a if i in b)) for a, b in map(split, packs)))
print(sum(prio(next(i for i in a if i in b and i in c))
          for a, b, c in group(packs)))
