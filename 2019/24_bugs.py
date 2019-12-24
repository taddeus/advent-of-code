#!/usr/bin/env python3
import sys
from collections import defaultdict

def read_grid(f):
    lines = [line.replace('\n', '') for line in f]
    return tuple(x == '#' for line in lines for x in line), len(lines[0])

def evolve_simple(grid, w):
    h = len(grid) // w

    def adjacent(i):
        y, x = divmod(i, w)
        nb = 0
        if x > 0:
            nb += grid[i - 1]
        if x < w - 1:
            nb += grid[i + 1]
        if y > 0:
            nb += grid[i - w]
        if y < h - 1:
            nb += grid[i + w]
        return nb

    def die_or_infest(i, bug):
        return adjacent(i) == 1 if bug else 1 <= adjacent(i) <= 2

    return tuple(die_or_infest(i, bug) for i, bug in enumerate(grid))

def find_recurring(grid, w):
    seen = set()
    while grid not in seen:
        seen.add(grid)
        grid = evolve_simple(grid, w)
    return grid

def biodiversity(grid):
    return sum(bug << i for i, bug in enumerate(grid))

def evolve_infinite(grid, w, minutes):
    l = len(grid)
    assert l == w * w
    mid = w // 2 * w + w // 2

    top_edge = tuple(range(w))
    bottom_edge = tuple(range(l - w, l))
    left_edge = tuple(range(0, l, w))
    right_edge = tuple(range(w - 1, l, w))

    def spread(x, y, nx, ny, level):
        ni = ny * w + nx
        if ni == mid:
            if x > nx:
                return right_edge, level + 1
            elif x < nx:
                return left_edge, level + 1
            elif y > ny:
                return bottom_edge, level + 1
            elif y < ny:
                return top_edge, level + 1
        elif nx == -1:
            return (mid - 1,), level - 1
        elif nx == w:
            return (mid + 1,), level - 1
        elif ny == -1:
            return (mid - w,), level - 1
        elif ny == w:
            return (mid + w,), level - 1
        else:
            return (ni,), level

    def neighbors(i, level):
        y, x = divmod(i, w)
        yield spread(x, y, x - 1, y, level)
        yield spread(x, y, x + 1, y, level)
        yield spread(x, y, x, y - 1, level)
        yield spread(x, y, x, y + 1, level)

    def evolve(bugs):
        adjacent = defaultdict(int)
        for i, level in bugs:
            y, x = divmod(i, w)
            for nbs, nblev in neighbors(i, level):
                for nb in nbs:
                    adjacent[(nb, nblev)] += 1
        return {x for x, a in adjacent.items()
                if a == 1 or (a == 2 and x not in bugs)}

    bugs = {(i, 0) for i, bug in enumerate(grid) if bug}
    while minutes > 0:
        bugs = evolve(bugs)
        minutes -= 1
    return len(bugs)

grid, w = read_grid(sys.stdin)
print(biodiversity(find_recurring(grid, w)))
print(evolve_infinite(grid, w, 200))
