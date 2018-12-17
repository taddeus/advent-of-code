#!/usr/bin/env python3
import sys

SAND, CLAY, DROP, STILL = 0, 1, 2, 4
WALL = CLAY | STILL
WATER = DROP | STILL

def parse():
    ranges = []
    for line in sys.stdin:
        x, y = line.rstrip().split(', ')
        if x[0] == 'y':
            x, y = y, x
        x = tuple(map(int, x[2:].split('..'))) if '..' in x else (int(x[2:]),) * 2
        y = tuple(map(int, y[2:].split('..'))) if '..' in y else (int(y[2:]),) * 2
        ranges.append(x + y)

    padding = 1
    xmin = min(min(min(r[:2]) for r in ranges), 500) - padding
    ymin = min(min(r[2:]) for r in ranges)
    ranges = [(xstart - xmin, xend - xmin, ystart - ymin, yend - ymin)
            for xstart, xend, ystart, yend in ranges]

    w = max(max(r[:2]) for r in ranges) + 1 + 2 * padding
    h = max(max(r[2:]) for r in ranges) + 1
    grid = w * h * [SAND]

    for xstart, xend, ystart, yend in ranges:
        for y in range(ystart, yend + 1):
            for x in range(xstart, xend + 1):
                grid[y * w + x] = CLAY

    grid[500 - xmin] = DROP
    return grid, w

def show(grid, w):
    source = grid.index(DROP)
    print('.' * source + '+' + '.' * (w - source - 1))
    for y in range(len(grid) // w):
        print(''.join('.#| ~'[x] for x in grid[y * w:(y + 1) * w]))

def flow(grid, w):
    h = len(grid) // w

    def expand(water, step):
        water += step
        while grid[water + w] & WALL and not grid[water] & WALL:
            water += step
        return water

    def drop(water):
        while water // w < h - 1:
            water += w

            if grid[water] == DROP:
                break
            elif grid[water] & WALL:
                # floor hit, rise while trapped between walls of clay
                lwall = rwall = True
                while lwall and rwall:
                    water -= w
                    left = expand(water, -1)
                    right = expand(water, 1)
                    lwall = grid[left] & WALL
                    rwall = grid[right] & WALL
                    fill = STILL if lwall and rwall else DROP
                    for i in range(left + 1, right):
                        grid[i] = fill

                # break condition above checks fow clay and water, but we only
                # keep flowing through sand
                lflow = grid[left] == SAND
                rflow = grid[right] == SAND

                if lflow and rflow:
                    # flow continues on both ends, fork
                    grid[left] = DROP
                    drop(left)
                    water = right
                elif lflow:
                    water = left
                elif rflow:
                    water = right
                else:
                    break

            # drop down
            grid[water] = DROP

    drop(grid.index(DROP))

grid, w = parse()
flow(grid, w)
#show(grid, w)
print(sum(1 for x in grid if x & WATER))
print(grid.count(STILL))
