#!/usr/bin/env python3
import sys
import re
from itertools import islice

W = 101
H = 103

def walk(robots):
    positions, velocities = zip(*((r[:2], r[2:]) for r in robots))
    while True:
        positions = [((x + dx) % W, (y + dy) % H)
                     for (x, y), (dx, dy) in zip(positions, velocities)]
        yield positions

def safety(positions):
    quadrants = [0, 0, 0, 0]
    midx = W // 2
    midy = H // 2
    for x, y in positions:
        if x != midx and y != midy:
            quadrants[(x > midx) + 2 * (y > midy)] += 1
    a, b, c, d = quadrants
    return a * b * c * d

def show(positions, start, stride):
    step = start
    for pos in map(set, islice(positions, start - 1, None, stride)):
        for y in range(H):
            print(''.join('.X'[(x, y) in pos] for x in range(W)))
        print('step', step)
        input('click ENTER for next step')
        step += stride

positions = walk(tuple(map(int, re.findall(r'-?\d+', line)))
                 for line in sys.stdin)
print(safety(next(islice(positions, 99, None, 1))))

#with open('input/14', 'r') as f:
#    robots = [tuple(map(int, re.findall(r'-?\d+', line))) for line in f]
#positions = walk(robots)
#show(positions, 129, 101)

# Easter egg looks like this in step 7502:
#
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# X.............................X
# X.............................X
# X.............................X
# X.............................X
# X..............X..............X
# X.............XXX.............X
# X............XXXXX............X
# X...........XXXXXXX...........X
# X..........XXXXXXXXX..........X
# X............XXXXX............X
# X...........XXXXXXX...........X
# X..........XXXXXXXXX..........X
# X.........XXXXXXXXXXX.........X
# X........XXXXXXXXXXXXX........X
# X..........XXXXXXXXX..........X
# X.........XXXXXXXXXXX.........X
# X........XXXXXXXXXXXXX........X
# X.......XXXXXXXXXXXXXXX.......X
# X......XXXXXXXXXXXXXXXXX......X
# X........XXXXXXXXXXXXX........X
# X.......XXXXXXXXXXXXXXX.......X
# X......XXXXXXXXXXXXXXXXX......X
# X.....XXXXXXXXXXXXXXXXXXX.....X
# X....XXXXXXXXXXXXXXXXXXXXX....X
# X.............XXX.............X
# X.............XXX.............X
# X.............XXX.............X
# X.............................X
# X.............................X
# X.............................X
# X.............................X
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
