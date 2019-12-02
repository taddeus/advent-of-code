#!/usr/bin/env python3
from itertools import dropwhile

illegal = tuple(map(ord, 'iol'))

def invalid(pw):
    pairs = 0
    prevpair = -1
    sequence = False

    for i in range(len(pw) - 2):
        a, b, c = pw[i:i + 3]
        if a in illegal:
            return True
        elif a == b and i >= prevpair + 2:
            pairs += 1
            prevpair = i
        elif a == b - 1 and b == c - 1:
            sequence = True

    return not sequence or pairs < 2

def convert(pw):
    return ''.join(chr(i + ord('a')) for i in pw[:-2])

def increment(pw):
    pw = [ord(c) - ord('a') for c in pw] + [-1, -1]
    while True:
        i = len(pw) - 3
        pw[i] += 1
        while pw[i] == 26:
            pw[i] = 0
            i -= 1
            pw[i] += 1
        yield pw

options = increment('cqjxjnds')
print(convert(next(dropwhile(invalid, options))))
print(convert(next(dropwhile(invalid, options))))
