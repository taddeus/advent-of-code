#!/usr/bin/env python3
import sys

FLOOR, EMPTY, OCCUPIED = range(3)

def parse(f):
    state = []
    for line in f:
        state += ['.L#'.index(c) for c in line.rstrip()]
        w = len(line.rstrip())
    return state, w

def changes(state, w, tolerance, see_far):
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
                   for dx in (-1, 0, 1)
                   for dy in (-1, 0, 1)
                   if dx or dy)

    for i, seat in enumerate(state):
        if seat == EMPTY and occupied_nb(i) == 0:
            yield i, OCCUPIED
        elif seat == OCCUPIED and occupied_nb(i) >= tolerance:
            yield i, EMPTY

def stabilize(state, w, tolerance, see_far):
    state = list(state)
    changeset = list(changes(state, w, tolerance, see_far))
    while changeset:
        for i, seat in changeset:
            state[i] = seat
        changeset[::] = changes(state, w, tolerance, see_far)
    return state

state, w = parse(sys.stdin)
print(stabilize(state, w, 4, False).count(OCCUPIED))
print(stabilize(state, w, 5, True).count(OCCUPIED))
