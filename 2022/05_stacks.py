#!/usr/bin/env python3
import sys

def parse(f):
    stacks = [[] for i in range(9)]
    moves = []

    for line in f:
        if line.startswith(' 1 '):
            break
        for i, crate in enumerate(line[1::4]):
            if crate != ' ':
                stacks[i].append(ord(crate))
    for stack in stacks:
        stack.reverse()

    next(f)
    for line in f:
        num, src, dst = map(int, line.split()[1::2])
        moves.append((num, src - 1, dst - 1))

    return stacks, moves

def move(stacks, moves, multipop):
    for num, src, dst in moves:
        popped = stacks[src][-num:]
        del stacks[src][-num:]
        if not multipop:
            popped.reverse()
        stacks[dst].extend(popped)
    return ''.join(chr(stack[-1]) for stack in stacks)

stacks, moves = parse(sys.stdin)
print(move(list(map(list, stacks)), moves, False))
print(move(stacks, moves, True))
