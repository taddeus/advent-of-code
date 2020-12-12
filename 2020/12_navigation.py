#!/usr/bin/env python3
import sys

WIND_DIRS = {'N': (0, 1), 'S': (0, -1), 'E': (1, 0), 'W': (-1, 0)}

def navigate(instructions, waypoint):
    x = y = 0
    dx, dy = (10, 1) if waypoint else WIND_DIRS['E']

    for inst, param in instructions:
        if inst == 'L':
            for i in range(param // 90):
                dx, dy = -dy, dx
        elif inst == 'R':
            for i in range(param // 90):
                dx, dy = dy, -dx
        elif inst == 'F':
            x += dx * param
            y += dy * param
        else:
            wdx, wdy = WIND_DIRS[inst]
            if waypoint:
                dx += wdx * param
                dy += wdy * param
            else:
                x += wdx * param
                y += wdy * param

    return abs(x) + abs(y)

instructions = [(line[0], int(line[1:])) for line in sys.stdin]
print(navigate(instructions, False))
print(navigate(instructions, True))
