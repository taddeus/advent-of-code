#!/usr/bin/env python3
import sys

dirs = {'<': (0, -1), '>': (0, 1), '^': (-1, 0), 'v': (1, 0)}
LEFT, STRAIGHT, RIGHT = 0, 1, 2
tracks = ''
carts = []
for y, line in enumerate(sys.stdin):
    for x, c in enumerate(line):
        if c in '<^>v':
            carts.append((y, x, *dirs[c], LEFT))
            tracks += '-' if c in '<>' else '|'
        else:
            tracks += c
h = y + 1
w = len(tracks) // h
firstcrash = None

while len(carts) > 1:
    crashed = set()

    for i, (y, x, dy, dx, nextturn) in enumerate(carts):
        y += dy
        x += dx
        track = tracks[y * w + x]

        for j, c in enumerate(carts):
            if c[:2] == (y, x):
                if firstcrash is None:
                    firstcrash = x, y
                crashed.add(i)
                crashed.add(j)

        if track == '\\':
            turn = LEFT if dy else RIGHT
        elif track == '/':
            turn = RIGHT if dy else LEFT
        elif track == '+':
            turn = nextturn
            nextturn = (nextturn + 1) % 3
        else:
            turn = STRAIGHT

        if turn == LEFT:
            dy, dx = -dx, dy
        elif turn == RIGHT:
            dy, dx = dx, -dy

        carts[i] = y, x, dy, dx, nextturn

    carts = sorted(c for i, c in enumerate(carts) if i not in crashed)

print(*firstcrash, sep=',')
y, x = carts[0][:2]
print(x, y, sep=',')
