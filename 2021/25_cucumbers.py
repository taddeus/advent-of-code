#!/usr/bin/env python3
import sys

def parse(content):
    return list(content.replace('\n', '')), content.find('\n')

def move(grid, w):
    h = len(grid) // w

    def right(i):
        y, x = divmod(i, w)
        return y * w + (x + 1) % w

    def down(i):
        y, x = divmod(i, w)
        return (y + 1) % h * w + x

    def move_axis(match, forward):
        can_move = [src for src, cell in enumerate(grid)
                    if cell == match and grid[forward(src)] == '.']
        for src in can_move:
            grid[forward(src)] = match
            grid[src] = '.'
        return bool(can_move)

    step = 1
    while move_axis('>', right) | move_axis('v', down):
        step += 1
    return step

print(move(*parse(sys.stdin.read())))
