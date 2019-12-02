#!/usr/bin/env python3
import sys
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
    dense = [reduce(xor, sparse[i:i + 16]) for i in range(0, 256, 16)]
    return ''.join('%02x' % d for d in dense)

# part 1
inp = sys.stdin.readline().rstrip()
sparse = list(range(256))
knot_round(sparse, map(int, inp.split(',')))
print(sparse[0] * sparse[1])

# part 2
assert knot_hash('') == 'a2582a3a0e66e6e86e3812dcb672a272'
assert knot_hash('AoC 2017') == '33efeb34ea91902bb2f59c9920caa6cd'
assert knot_hash('1,2,3') == '3efbe78a8d82f29979031a4aa0b16a9d'
assert knot_hash('1,2,4') == '63960835bcdc130f0b66d7ff4f6a5a8e'
print(knot_hash(inp))
