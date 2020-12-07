#!/usr/bin/env python3
import sys

def parse(f):
    cur = []
    for line in f:
        if line == '\n':
            yield cur
            cur = []
        else:
            cur.append(line.rstrip())
    yield cur

groups = list(parse(sys.stdin))
print(sum(len(set.union(*map(set, g))) for g in groups))
print(sum(len(set.intersection(*map(set, g))) for g in groups))
