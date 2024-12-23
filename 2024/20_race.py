#!/usr/bin/env python3
import sys

def parse_track(f):
    grid = [line.rstrip() for line in f]
    x, y = next((x, y) for y, row in enumerate(grid)
                for x, cell in enumerate(row) if cell == 'S')
    track = [None, (x, y)]
    while grid[y][x] != 'E':
        x, y = next(nb for nb in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1))
                    if nb != track[-2] and grid[nb[1]][nb[0]] != '#')
        track.append((x, y))
    return track[1:]

def cheats(track, max_dist):
    for (t1, (x1, y1)) in enumerate(track):
        for t2 in range(t1 + 3, len(track)):
            x2, y2 = track[t2]
            dist = abs(x2 - x1) + abs(y2 - y1)
            if dist <= max_dist and t2 - t1 > dist:
                yield t2 - t1 - dist

track = parse_track(sys.stdin)
print(sum(saved >= 100 for saved in cheats(track, 2)))
print(sum(saved >= 100 for saved in cheats(track, 20)))
