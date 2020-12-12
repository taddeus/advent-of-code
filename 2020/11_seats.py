#!/usr/bin/env python3
import sys

FLOOR, EMPTY, OCCUPIED = '.L#'

def parse(f):
    grid = f.read().rstrip()
    return grid.replace('\n', ''), grid.find('\n')

def evolve(state, w, tolerance, see_far):
    h = len(state) // w

    def see_occupied(x, y, dx, dy):
        x += dx
        y += dy
        if x < 0 or x >= w or y < 0 or y >= h:
            return False
        seat = state[y * w + x]
        if seat != FLOOR:
            return seat == OCCUPIED
        return see_far and see_occupied(x, y, dx, dy)

    def occupied_nb(i):
        y, x = divmod(i, w)
        return sum(see_occupied(x, y, dx, dy)
                   for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy)

    for i, seat in enumerate(state):
        if seat == EMPTY and occupied_nb(i) == 0:
            yield OCCUPIED
        elif seat == OCCUPIED and occupied_nb(i) >= tolerance:
            yield EMPTY
        else:
            yield seat

def stabilize(state, *args):
    prev = None
    while state != prev:
        prev = state
        state = ''.join(evolve(state, *args))
    return state

state, w = parse(sys.stdin)
print(stabilize(state, w, 4, False).count(OCCUPIED))
print(stabilize(state, w, 5, True).count(OCCUPIED))
