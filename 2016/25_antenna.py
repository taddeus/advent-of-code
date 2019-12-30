#!/usr/bin/env python3
import sys
from itertools import count, islice

def read_program(f):
    maybe_int = lambda x: int(x) if x.isdigit() or x[0] == '-' else x
    for line in f:
        instr = tuple(map(maybe_int, line.split()))
        yield instr + (None,) * (3 - len(instr))

def check_mul(p, pc):
    if pc <= len(p) - 5:
        opcodes, a, b = zip(*p[pc:pc + 5])
        if a[1] == a[2] and a[3] == a[4] and b[2] == -2 and b[4] == -5:
            if opcodes == ('inc', 'dec', 'jnz', 'dec', 'jnz'):
                return a[1], a[3]

def run(p, init):
    regs = [init, 0, 0, 0]
    pc = 0

    def load(x):
        return x if isinstance(x, int) else regs[ord(x) - ord('a')]

    def store(reg, value):
        regs[ord(reg) - ord('a')] = value

    while pc < len(p):
        opcode, a, b = p[pc]
        if opcode == 'cpy':
            store(b, load(a))
        elif opcode == 'inc':
            params = check_mul(p, pc)
            if params:
                reg1, reg2 = params
                increment = load(reg1) * load(reg2)
                store(reg1, 0)
                store(reg2, 0)
                pc += 4
            else:
                increment = 1
            store(a, load(a) + increment)
        elif opcode == 'dec':
            store(a, load(a) - 1)
        elif opcode == 'jnz':
            if load(a):
                pc += load(b) - 1
        elif opcode == 'out':
            yield load(a)
        pc += 1

    return regs[0]

def is_clock(signal):
    expect = 0
    for x in islice(signal, 8):
        if x != expect:
            return False
        expect = 1 - expect
    return True

def find_clock(p):
    for a in count(0):
        if is_clock(run(p, a)):
            return a

program = list(read_program(sys.stdin))
print(find_clock(program))
