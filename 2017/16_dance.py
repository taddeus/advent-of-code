#!/usr/bin/env python3
import sys
from functools import partial

def init():
    # 16 4-bit dancers in a 64-bit number
    return 0xfedcba9876543210

def spin(n, dancers):
    nbits = 64 - n * 4
    mask_first = (1 << nbits) - 1
    mask_last = (1 << 64) - (1 << nbits)
    first = dancers & mask_first
    last = dancers & mask_last
    return (first << (64 - nbits)) | (last >> nbits)

def swap_indices(i, j, dancers):
    if j < i:
        return swap_indices(j, i, dancers)

    a = dancers & (0xf << (4 * i))
    b = dancers & (0xf << (4 * j))
    rest = dancers ^ a ^ b
    diff = 4 * (j - i)
    return rest | (a << diff) | (b >> diff)

def swap_values(a, b, dancers):
    return swap_indices(index(a, dancers), index(b, dancers), dancers)

def index(ident, dancers):
    i = 0
    while dancers & 0xf != ident:
        dancers >>= 4
        i += 1
    return i

def stringify(dancers):
    s = ''
    for i in range(16):
        ident = dancers & 0xf
        dancers >>= 4
        s += chr(ident + ord('a'))
    return s

def parse(f):
    for move in f.readline().rstrip().split(','):
        if move[0] == 's':
            yield partial(spin, int(move[1:]))
        elif move[0] == 'x':
            i, j = move[1:].split('/')
            yield partial(swap_indices, int(i), int(j))
        elif move[0] == 'p':
            a, b = move[1:].split('/')
            yield partial(swap_values, ord(a) - ord('a'), ord(b) - ord('a'))

def move_all(moves, dancers):
    for move in moves:
        dancers = move(dancers)
    return dancers

def dance_many_times(dance, times):
    dancers = init()
    seen = set()
    patlen = 0
    while dancers not in seen:
        seen.add(dancers)
        dancers = dance(dancers)
        patlen += 1
    for i in range(times % patlen):
        dancers = dance(dancers)
    return dancers

# part 1
dance = partial(move_all, list(parse(sys.stdin)))
print(stringify(dance(init())))

# part 2
print(stringify(dance_many_times(dance, 1000000000)))
