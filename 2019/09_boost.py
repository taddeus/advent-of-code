#!/usr/bin/env python3
import sys
from operator import add, mul, lt, eq

def run(p, inputs, memsize=0):
    opmap = {1: add, 2: mul, 7: lt, 8: eq}
    p = p + [0] * memsize
    pc = relbase = 0

    while p[pc] != 99:
        modes, opcode = divmod(p[pc], 100)

        def decode_param(offset):
            return p[pc + offset], modes // (10 ** (offset - 1)) % 10

        def pload(offset):
            param, mode = decode_param(offset)
            return param if mode == 1 else p[param + relbase * mode // 2]

        def pstore(offset, value):
            param, mode = decode_param(offset)
            p[param + relbase * mode // 2] = value

        if opcode in (1, 2, 7, 8):
            pstore(3, opmap[opcode](pload(1), pload(2)))
            pc += 4
        elif opcode == 3:
            pstore(1, inputs.pop())
            pc += 2
        elif opcode == 4:
            yield pload(1)
            pc += 2
        elif opcode == 5:
            pc = pload(2) if pload(1) else pc + 3
        elif opcode == 6:
            pc = pload(2) if not pload(1) else pc + 3
        elif opcode == 9:
            relbase += pload(1)
            pc += 2

program = list(map(int, sys.stdin.read().split(',')))
print(next(run(program, [1], 10000)))
print(next(run(program, [2], 10000)))
