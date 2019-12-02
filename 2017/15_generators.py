#!/usr/bin/env python3
def gen(seed, factor, mul=1):
    num = seed
    while True:
        num = (num * factor) % 2147483647
        if num % mul == 0:
            yield num & 0xffff

# part 1
a = gen(116, 16807)
b = gen(299, 48271)
print(sum(int(next(a) == next(b)) for i in range(40000000)))

# part 2
a = gen(116, 16807, 4)
b = gen(299, 48271, 8)
print(sum(int(next(a) == next(b)) for i in range(5000000)))
