#!/usr/bin/env python3
import sys

def run(p, inputs):
    pc = 0
    while p[pc] != 99:
        modes, opcode = divmod(p[pc], 100)

        def modeswitch(offset):
            value = p[pc + offset]
            mode = modes // (10 ** (offset - 1)) % 10
            return value if mode else p[value]

        if opcode in (1, 2):
            a = modeswitch(1)
            b = modeswitch(2)
            out = p[pc + 3]
            p[out] = a + b if opcode == 1 else a * b
            pc += 4
        elif opcode == 3:
            address = p[pc + 1]
            p[address] = inputs.pop()
            pc += 2
        elif opcode == 4:
            yield modeswitch(1)
            pc += 2
        elif opcode == 5:
            pc = modeswitch(2) if modeswitch(1) else pc + 3
        elif opcode == 6:
            pc = modeswitch(2) if not modeswitch(1) else pc + 3
        elif opcode in (7, 8):
            a = modeswitch(1)
            b = modeswitch(2)
            out = p[pc + 3]
            p[out] = int(a < b if opcode == 7 else a == b)
            pc += 4

def initrun(p, inp):
    return list(run(list(p), list(inp)))

program = list(map(int, sys.stdin.read().split(',')))
print(initrun(program, [1])[-1])
print(initrun(program, [5])[-1])
