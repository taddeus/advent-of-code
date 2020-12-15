#!/usr/bin/env python3
def gen(start):
    yield from start
    spoken = {n: i for i, n in enumerate(start)}
    i = len(start)
    num = 0
    while True:
        yield num
        nextnum = i - spoken.get(num, i)
        spoken[num] = i
        num = nextnum
        i += 1

def nth(start, n):
    return next(num for i, num in enumerate(gen(start)) if i == n - 1)

start = [13, 0, 10, 12, 1, 5, 8]
print(nth(start, 2020))
print(nth(start, 30000000))
