#!/usr/bin/env python3
import sys

def read_program(f):
    maybe_int = lambda x: int(x) if x.isdigit() or x[0] == '-' else x
    for line in f:
        yield tuple(map(maybe_int, line.split()))

def run(p, init):
    regs = [0, 0, init, 0]
    pc = 0

    def load(x):
        return x if isinstance(x, int) else regs[ord(x) - ord('a')]

    def store(reg, value):
        regs[ord(reg) - ord('a')] = value

    while pc < len(p):
        instr = p[pc]
        opcode = instr[0]
        if opcode == 'cpy':
            src, dst = instr[1:]
            store(dst, load(src))
        elif opcode == 'inc':
            reg = instr[1]
            store(reg, load(reg) + 1)
        elif opcode == 'dec':
            reg = instr[1]
            store(reg, load(reg) - 1)
        elif opcode == 'jnz':
            pred, offset = instr[1:]
            if load(pred):
                pc += load(offset) - 1
        pc += 1

    return regs[0]

program = list(read_program(sys.stdin))
print(run(program, 0))
print(run(program, 1))
