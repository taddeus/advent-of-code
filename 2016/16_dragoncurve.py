#!/usr/bin/env python3
def fill(seed, target):
    curve = [False] * target
    for i, bit in enumerate(seed):
        curve[i] = bit == '1'
    length = len(seed)
    while length < target:
        for i in range(max(0, length * 2 + 1 - target), length):
            curve[length * 2 - i] = not curve[i]
        length = length * 2 + 1
    return curve

def checksum(curve):
    length = len(curve)
    while length % 2 == 0:
        for i in range(length // 2):
            curve[i] = curve[i * 2] == curve[i * 2 + 1]
        length >>= 1
    return curve[:length]

def joinbits(curve):
    return ''.join('01'[bit] for bit in curve)

print(joinbits(checksum(fill('01110110101001000', 272))))
print(joinbits(checksum(fill('01110110101001000', 35651584))))
