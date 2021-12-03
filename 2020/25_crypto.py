#!/usr/bin/env python3
def transform(n, loopsize):
    return pow(n, loopsize, 20201227)

def loopsize(transformed):
    n = 1
    size = 0
    while n != transformed:
        n = n * 7 % 20201227
        size += 1
    return size

print(transform(9789649, loopsize(3647239)))
