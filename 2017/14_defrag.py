#!/usr/bin/env python3
from functools import reduce
from operator import xor

def knot_round(nums, lengths, pos=0, skip=0, n=256):
    for length in lengths:
        for i in range(length // 2):
            left = (pos + i) % n
            right = (pos + length - i - 1) % n
            nums[left], nums[right] = nums[right], nums[left]

        pos = (pos + length + skip) % n
        skip = (skip + 1) % n

    return pos, skip

def knot_hash(inp, rounds=64):
    lengths = tuple(map(ord, inp)) + (17, 31, 73, 47, 23)
    pos = skip = 0
    sparse = list(range(256))
    for r in range(rounds):
        pos, skip = knot_round(sparse, lengths, pos, skip)
    dense = 0
    for i in range(0, 256, 16):
        group = reduce(xor, sparse[i:i + 16])
        dense = (dense << 8) | group
    return dense

def hamming_weight(n):
    return sum((n >> i) & 1 for i in range(n.bit_length()))

def used_squares(key):
    return sum(hamming_weight(knot_hash(f'{key}-{i}')) for i in range(128))

def used_regions(key):
    grid = []
    for y in range(128):
        h = knot_hash(f'{key}-{y}')
        grid.extend(-((h >> i) & 1) for i in range(128))

    def spread(x, y, region):
        i = y * 128 + x
        if grid[i] == -1:
            grid[i] = region
            if x > 0:
                spread(x - 1, y, region)
            if x < 127:
                spread(x + 1, y, region)
            if y > 0:
                spread(x, y - 1, region)
            if y < 127:
                spread(x, y + 1, region)

    region = 1
    for i, cell in enumerate(grid):
        if cell == -1:
            y, x = divmod(i, 128)
            spread(x, y, region)
            region += 1

    return region - 1

print(used_squares('ljoxqyyw'))
print(used_regions('ljoxqyyw'))
