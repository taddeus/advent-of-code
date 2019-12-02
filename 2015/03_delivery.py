#!/usr/bin/env python3
import sys
moves = sys.stdin.readline().rstrip()
diffs = {'^': (0, -1), 'v': (0,  1), '>': ( 1, 0), '<': (-1, 0)}

def visit(n):
    visited = set([(0, 0)])
    locs = [(0, 0)] * n
    turn = 0
    for move in moves:
        x, y = locs[turn]
        dx, dy = diffs[move]
        x += dx
        y += dy
        visited.add((x, y))
        locs[turn] = x, y
        turn = (turn + 1) % n
    return len(visited)

print(visit(1))
print(visit(2))
