#!/usr/bin/env python3
import sys
from heapq import heappop, heappush

def shortest_path(falls):
    work = [(0, ((0, 0),))]
    dist = {(0, 0): 0}
    while work:
        length, path = heappop(work)
        x, y = path[-1]
        if dist[x, y] != length:
            continue
        if x == 70 and y == 70:
            return set(path)
        for nb in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            nx, ny = nb
            if 0 <= nx <= 70 and 0 <= ny <= 70 and nb not in falls and \
                    dist.get(nb, 1e4) > length + 1:
                dist[nb] = length + 1
                heappush(work, (length + 1, path + (nb,)))

falls = [tuple(map(int, line.split(','))) for line in sys.stdin]
cur = set(falls[:1024])
path = shortest_path(cur)
print(len(path) - 1)
for fall in falls[1024:]:
    cur.add(fall)
    if fall in path:
        path = shortest_path(cur)
        if path is None:
            print('%d,%d' % fall)
            break
