#!/usr/bin/env python3
import sys
from itertools import islice, takewhile

def parse(f):
    rows = (l[1::4] for l in takewhile(lambda l: not l.startswith(' 1'), f))
    yield [[ord(c) for c in reversed(col) if c != ' '] for col in zip(*rows)]
    yield [(int(num), int(src) - 1, int(dst) - 1)
           for (_, num, _, src, _, dst) in map(str.split, islice(f, 1, None))]

def move(stacks, moves, multipop):
    for num, src, dst in moves:
        popped = stacks[src][-num:]
        del stacks[src][-num:]
        stacks[dst].extend(popped if multipop else reversed(popped))
    return ''.join(chr(stack[-1]) for stack in stacks)

stacks, moves = parse(sys.stdin)
print(move(list(map(list, stacks)), moves, False))
print(move(stacks, moves, True))
