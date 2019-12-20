#!/usr/bin/env python3
import sys
from collections import deque
from itertools import chain

def read_grid(f):
    rows = [line.replace('\n', '') for line in f]
    return list(chain.from_iterable(rows)), len(rows[0])

def find_labels(grid, w):
    def get(i):
        return grid[i] if 0 <= i < len(grid) else ' '

    def try_label(i, spacediff, outer):
        if get(i + spacediff) == '.':
            labels.setdefault(label, []).append((i, i + spacediff, outer))

    labels = {}
    h = len(grid) // w

    for i, cell in enumerate(grid):
        if cell.isalpha():
            y, x = divmod(i, w)

            label = get(i) + get(i + 1)
            if label.isalpha():
                try_label(i, -1, x > w // 2)
                try_label(i + 1, 1, x < w // 2)

            label = get(i) + get(i + w)
            if label.isalpha():
                try_label(i, -w, y > h // 2)
                try_label(i + w, w, y < h // 2)

    return labels

def find_portals(labels):
    assert all(len(v) == 2 for v in labels.values())
    inner = {}
    outer = {}
    for (l1, s1, o1), (l2, s2, o2) in labels.values():
        assert o1 ^ o2
        (outer if o1 else inner)[l1] = s2
        (outer if o2 else inner)[l2] = s1
    return inner, outer

def shortest_path(grid, w, leveldiff):
    labels = find_labels(grid, w)
    src = labels.pop('AA')[0][1]
    dst = labels.pop('ZZ')[0][1]
    inner, outer = find_portals(labels)
    work = deque([(src, 0, 0)])
    visited = set()

    while work:
        i, dist, level = work.popleft()
        if i == dst and level == 0:
            return dist
        if (i, level) in visited:
            continue
        visited.add((i, level))
        for nb in (i - 1, i + 1, i - w, i + w):
            if grid[nb] == '.':
                work.append((nb, dist + 1, level))
            elif nb in inner:
                work.append((inner[nb], dist + 1, level + leveldiff))
            elif nb in outer and level > 0:
                work.append((outer[nb], dist + 1, level - leveldiff))

grid, w = read_grid(sys.stdin)
print(shortest_path(grid, w, 0))
print(shortest_path(grid, w, 1))
