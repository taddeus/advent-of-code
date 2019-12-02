#!/usr/bin/env python3
import sys

def get_code(instructions, trans):
    cur = '5'
    code = ''
    for line in instructions:
        for c in line.rstrip():
            cur = trans[c].get(cur, cur)
        code += cur
    return code


def maketrans(short):
    return {x[0]: x[1] for x in short.split()}


trans_square = {
    'U': maketrans('41 52 63 74 85 96'),
    'D': maketrans('14 25 36 47 58 69'),
    'L': maketrans('21 32 54 65 87 98'),
    'R': maketrans('12 23 45 56 78 89')
}

trans_diamond = {
    'U': maketrans('31 62 73 84 A6 B7 C8 DB'),
    'D': maketrans('13 26 37 48 6A 7B 8C BD'),
    'L': maketrans('32 43 65 76 87 98 BA CB'),
    'R': maketrans('23 34 56 67 78 89 AB BC')
}

instructions = sys.stdin.readlines()
print(get_code(instructions, trans_square))
print(get_code(instructions, trans_diamond))
