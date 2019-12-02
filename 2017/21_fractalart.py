#!/usr/bin/env python3
import sys
from itertools import islice


def parse(f):
    def vflip(pat):
        return '/'.join(pat.split('/')[::-1])

    def hflip(pat):
        return '/'.join(l[::-1] for l in pat.split('/'))

    def rotate(pat):
        return '/'.join(''.join(l[::-1]) for l in zip(*pat.split('/')))

    rules = {}

    for line in f:
        pat, rep = line.rstrip().split(' => ')

        for pat in (pat, vflip(pat), hflip(pat)):
            rules[pat] = rep
            for i in range(3):
                pat = rotate(pat)
                rules[pat] = rep

    return rules


def sqsplit(grid, w, sqsize):
    for y in range(0, w, sqsize):
        for x in range(0, w, sqsize):
            i = y * w + x
            yield '/'.join(grid[i + n * w:i + n * w + sqsize]
                           for n in range(sqsize))


def sqjoin(squares, w, sqsize, rules):
    squares = iter(squares)
    grid = ''

    for y in range(0, w, sqsize):
        row = islice(squares, w // sqsize)
        grid += ''.join(i for l in zip(*[sq.split('/') for sq in row]) for i in l)

    return grid


def grow(grid, w, rules):
    sqsize = 2 + (w % 2)
    wnew = w + w // sqsize
    squares = sqsplit(grid, w, sqsize)
    transformed = (rules[sq] for sq in squares)
    return sqjoin(transformed, wnew, sqsize + 1, rules), wnew


w = 3
grid = '.#...####'
rules = parse(sys.stdin)

for i in range(5):
    grid, w = grow(grid, w, rules)
print(grid.count('#'))

for i in range(13):
    grid, w = grow(grid, w, rules)
print(grid.count('#'))
