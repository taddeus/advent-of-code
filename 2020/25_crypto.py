#!/usr/bin/env python3
def transform(n, loopsize):
    return pow(n, loopsize, 20201227)

def loopsize(transformed):
    n = size = 1
    while True:
        n = n * 7 % 20201227
        if n == transformed:
            return size
        size += 1

a, b = 9789649, 3647239
print(transform(a, loopsize(b)))
