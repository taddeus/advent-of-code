#!/usr/bin/env python3
import sys
from heapq import heappop, heappush

def parse(f):
    assert f.readline() == '#############\n'
    hallway = f.readline().rstrip().replace('#', '')
    top = f.readline().rstrip().replace('#', '')
    bottom = f.readline().strip().replace('#', '')
    return ''.join(map(''.join, zip(top, bottom))) + hallway

def swap(s, i, j):
    if i > j: i, j = j, i
    return s[:i] + s[j] + s[i + 1:j] + s[i] + s[j + 1:]

def walk(src, dst):
    step = -1 if src > dst else 1
    return range(src + step, dst + step, step)

def into_hallway(state, door, rsize):
    first_door = 4 * rsize + 2
    doors = tuple(range(first_door, first_door + 8, 2))

    for end in (4 * rsize, len(state) - 1):
        for dist, i in enumerate(walk(door, end)):
            if state[i] != '.':
                break
            if i not in doors:
                yield dist + 1, i

def steps(state, rsize):
    for room, expect in zip(range(0, 4 * rsize, rsize), 'ABCD'):
        door = 4 * rsize + 2 * (room // rsize + 1)
        for depth, cell in enumerate(state[room:room + rsize]):
            if cell != '.':
                if cell != expect or any(state[room + d] != expect
                                         for d in range(depth + 1, rsize)):
                    for door_dist, hall in into_hallway(state, door, rsize):
                        yield door_dist + depth + 1, room + depth, hall
                break

    for hall in range(4 * rsize, len(state)):
        apod = state[hall]
        if apod != '.':
            room = 'ABCD'.index(apod) * rsize
            door = 4 * rsize + 2 * (room // rsize + 1)
            if all(state[i] == '.' for i in walk(hall, door)):
                door_dist = abs(hall - door)
                for depth in range(rsize - 1, -1, -1):
                    cell = state[room + depth]
                    if cell == '.':
                        yield door_dist + depth + 1, hall, room + depth
                    elif cell != apod:
                        break

def organize(state, rsize):
    work = [(0, state)]
    seen = {state: 0}
    final = ''.join(x * rsize for x in 'ABCD') + '...........'
    while work:
        energy, state = heappop(work)
        if state == final:
            return energy
        for dist, src, dst in steps(state, rsize):
            moved = swap(state, src, dst)
            moved_energy = energy + dist * 10 ** 'ABCD'.index(state[src])
            if seen.get(moved, 1 << 32) > moved_energy:
                heappush(work, (moved_energy, moved))
                seen[moved] = moved_energy

def extend(state, insert):
    return ''.join(state[2 * i] + ext + state[2 * i + 1]
                   for i, ext in enumerate(insert)) + state[8:]

state = parse(sys.stdin)
print(organize(state, 2))
print(organize(extend(state, ('DD', 'CB', 'BA', 'AC')), 4))
