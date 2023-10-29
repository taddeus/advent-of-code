#!/usr/bin/env python3
import sys
from heapq import heappop, heappush
from math import lcm

def parse(inp):
    blizzards = {}
    DELTA = (1, 0), (-1, 0), (0, 1), (0, -1)
    for y, line in enumerate(inp):
        for x, cell in enumerate(line.rstrip()):
            if cell not in '#.':
                d = DELTA['><v^'.index(cell)]
                blizzards.setdefault((x - 1, y - 1), []).append(d)
    return blizzards, x - 1, y - 1

def move(blizzards, w, h):
    for _ in range(lcm(w, h)):
        yield set(blizzards)
        newbliz = {}
        for (x, y), deltas in blizzards.items():
            for dx, dy in deltas:
                moved = (x + dx + w) % w, (y + dy + h) % h
                newbliz.setdefault(moved, []).append((dx, dy))
        blizzards = newbliz

def walk(src, dst, step, blizzard_movement, w, h):
    start = src, step
    visited = {start}
    dist = {start: 0}
    work = [(0, start)]
    endx, endy = dst

    while work:
        pos, step = current = heappop(work)[1]
        if pos == dst:
            return step
        x, y = pos
        bliz = blizzard_movement[(step + 1) % len(blizzard_movement)]
        for dx, dy in ((-1, 0), (1, 0), (0, 0), (0, -1), (0, 1)):
            nx = x + dx
            ny = y + dy
            if (0 <= nx < w and 0 <= ny < h and (nx, ny) not in bliz) or \
                    (nx == w - 1 and ny == h) or (nx == 0 and ny == -1):
                nb = (nx, ny), step + 1
                if nb not in visited:
                    visited.add(nb)
                    alt = dist[current] + 1
                    if alt < dist.get(nb, 1000000):
                        dist[nb] = alt
                        estimate = abs(endx - nx) + abs(endy - ny)
                        heappush(work, (alt + estimate, nb))

blizzards, w, h = parse(sys.stdin)
blizzard_movement = list(move(blizzards, w, h))
start = 0, -1
end = w - 1, h
to_end = walk(start, end, 0, blizzard_movement, w, h)
print(to_end)
to_start = walk(end, start, to_end, blizzard_movement, w, h)
print(walk(start, end, to_start, blizzard_movement, w, h))
