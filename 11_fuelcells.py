#!/usr/bin/env python3
serial = 5791
w = 300
grid = w * w * [0]

for y in range(w):
    for x in range(w):
        rack = x + 11
        grid[y * w + x] = (rack * (y + 1) + serial) * rack // 100 % 10 - 5

for i in range(len(grid)):
    y, x = divmod(i, w)
    top = grid[i - w] if y else 0
    left = grid[i - 1] if x else 0
    topleft = grid[i - w - 1] if x and y else 0
    grid[i] += top + left - topleft

def squares(sz):
    for y in range(w - sz + 1):
        for x in range(w - sz + 1):
            s = grid[(y + sz - 1) * w + (x + sz - 1)]
            if y and x: s += grid[(y - 1) * w + (x - 1)]
            if x: s -= grid[(y + sz - 1) * w + (x - 1)]
            if y: s -= grid[(y - 1) * w + (x + sz - 1)]
            yield s, x + 1, y + 1

s, x, y = max(squares(3))
print(x, y, sep=',')

s, x, y, sz = max(max(squares(sz)) + (sz,) for sz in range(1, w + 1))
print(x, y, sz, sep=',')
