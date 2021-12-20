#!/usr/bin/env python3
import sys
from itertools import islice, starmap
from operator import add, mul, gt, lt, eq
from functools import reduce

def bitstream(hexdata):
    for quad in hexdata:
        i = int(quad, 16)
        yield i >> 3
        yield i >> 2 & 1
        yield i >> 1 & 1
        yield i & 1

def consume(bits, num):
    i = 0
    for bit in islice(bits, num):
        i = i << 1 | bit
    return i

def decode(bits):
    while True:
        try:
            version = consume(bits, 3)
            ty = consume(bits, 3)

            if ty == 4:
                has_next = next(bits)
                arg = consume(bits, 4)
                while has_next:
                    has_next = next(bits)
                    arg = arg << 4 | consume(bits, 4)
            elif next(bits):
                arg = list(islice(decode(bits), consume(bits, 11)))
            else:
                arg = list(decode(islice(bits, consume(bits, 15))))

            yield ty, version, arg
        except StopIteration:
            break

def version_sum(ty, version, arg):
    return version if ty == 4 else version + sum(starmap(version_sum, arg))

OPS = add, mul, min, max, None, gt, lt, eq

def evaluate(ty, version, arg):
    return arg if ty == 4 else reduce(OPS[ty], starmap(evaluate, arg))

packet = next(decode(bitstream(sys.stdin.readline().rstrip())))
print(version_sum(*packet))
print(evaluate(*packet))
