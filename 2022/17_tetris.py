#!/usr/bin/env python3
import sys
from itertools import cycle
from operator import sub

ROCKS = (
    (1, ((0, 0), (1, 0), (2, 0), (3, 0))),
    (3, ((1, 0), (0, 1), (1, 1), (2, 1), (1, 2))),
    (3, ((0, 0), (1, 0), (2, 0), (2, 1), (2, 2))),
    (4, ((0, 0), (0, 1), (0, 2), (0, 3))),
    (2, ((0, 0), (1, 0), (0, 1), (1, 1))),
)

def drop_rocks(shifts, n):
    shifts = cycle(enumerate(shifts))
    tower = set()

    def drop(rock, height):
        x = 2
        y = height + 3
        for shift_id, shift in shifts:
            if all(0 <= x + dx + shift < 7
                   and (x + dx + shift, y + dy) not in tower
                   for dx, dy in rock):
                x += shift
            if any((x + dx, y + dy - 1) in tower or y == 0
                   for dx, dy in rock):
                return x, y, shift_id
            y -= 1

    def dropn(n, height):
        cache = {}
        loop_size = 0

        while not loop_size:
            key = ()
            for rock_height, rock in ROCKS:
                x, y, shift_id = drop(rock, height)
                tower.update({(x + dx, y + dy) for dx, dy in rock})
                height = max(height, y + rock_height)
                n -= 1
                if n == 0:
                    return height
                key += shift_id,

            value = n, height
            loop_size, diff = map(sub, cache.setdefault(key, value), value)

        skip, n = divmod(n, loop_size)
        return dropn(n, height) - skip * diff

    return dropn(n, 0)

shifts = ['< >'.index(x) - 1 for x in sys.stdin.readline().rstrip()]
print(drop_rocks(shifts, 2022))
print(drop_rocks(shifts, 1000000000000))
