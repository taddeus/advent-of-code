#!/usr/bin/env python3
import sys
from collections import defaultdict, deque
from operator import add, mul, lt, eq
from time import sleep

def run(p, get_input, memsize=0):
    def decode_param(offset):
        return p[pc + offset], modes // (10 ** (offset - 1)) % 10

    def pload(offset):
        param, mode = decode_param(offset)
        return param if mode == 1 else p[param + relbase * mode // 2]

    def pstore(offset, value):
        param, mode = decode_param(offset)
        p[param + relbase * mode // 2] = value

    opmap = {1: add, 2: mul, 7: lt, 8: eq}
    p = p + [0] * memsize
    pc = relbase = 0

    while p[pc] != 99:
        modes, opcode = divmod(p[pc], 100)

        if opcode in (1, 2, 7, 8):
            pstore(3, opmap[opcode](pload(1), pload(2)))
            pc += 4
        elif opcode == 3:
            pstore(1, get_input())
            pc += 2
        elif opcode == 4:
            yield pload(1)
            pc += 2
        elif opcode == 5:
            pc = pload(2) if pload(1) else pc + 3
        elif opcode == 6:
            pc = pload(2) if not pload(1) else pc + 3
        elif opcode == 9:
            relbase += pload(1)
            pc += 2

NORTH, SOUTH, EAST, WEST = range(1, 5)
WALL, SPACE, OXYGEN, UNKOWN = range(4)
DX = [0, 0, -1, 1]
DY = [-1, 1, 0, 0]

def draw(mapped, robot):
    if '-v' not in sys.argv:
        return

    def draw_pos(pos):
        return 'D' if pos == robot else '#.O '[mapped.get(pos, UNKOWN)]

    minx = min(x for x, y in mapped)
    maxx = max(x for x, y in mapped)
    miny = min(y for y, y in mapped)
    maxy = max(y for y, y in mapped)

    print('\033c', end='')
    for y in range(miny, maxy + 1):
        print(''.join(draw_pos((x, y)) for x in range(minx, maxx + 1)))
    sleep(.001)

def map_area(program):
    reverse_dir = [SOUTH, NORTH, WEST, EAST]

    pos = 0, 0
    direction = NORTH
    control = run(program, lambda: direction, 0)
    mapped = {pos: SPACE}
    path = [(NORTH, pos)]
    oxygen_distance = None

    def pick_direction():
        x, y = pos
        for d in (NORTH, SOUTH, EAST, WEST):
            newpos = x + DX[d - 1], y + DY[d - 1]
            if newpos not in mapped:
                return False, (d, newpos)
        return True, path.pop()

    while len(path):
        backtrack, (direction, newpos) = pick_direction()
        status = next(control)
        mapped[newpos] = status
        if status != WALL:
            if not backtrack:
                path.append((reverse_dir[direction - 1], pos))
            pos = newpos

            if status == OXYGEN:
                oxygen_distance = len(path) - 1
        draw(mapped, pos)

    return oxygen_distance, mapped

def spread_oxygen(mapped):
    frontier = set(pos for pos, status in mapped.items() if status == OXYGEN)
    minutes = -1
    while frontier:
        newfrontier = set()
        for x, y in frontier:
            mapped[(x, y)] = OXYGEN
            for d in range(4):
                nb = x + DX[d], y + DY[d]
                if mapped[nb] == SPACE:
                    newfrontier.add(nb)
        minutes += 1
        frontier = newfrontier
        draw(mapped, None)
    return minutes

program = list(map(int, sys.stdin.readline().split(',')))
oxygen_distance, mapped = map_area(program)
print(oxygen_distance)
print(spread_oxygen(mapped))
