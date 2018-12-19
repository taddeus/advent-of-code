#!/usr/bin/env python3
import sys

isa = {
    'addr': lambda a, b, reg: reg[a] + reg[b],
    'addi': lambda a, b, reg: reg[a] + b,
    'mulr': lambda a, b, reg: reg[a] * reg[b],
    'muli': lambda a, b, reg: reg[a] * b,
    'banr': lambda a, b, reg: reg[a] & reg[b],
    'bani': lambda a, b, reg: reg[a] & b,
    'borr': lambda a, b, reg: reg[a] | reg[b],
    'bori': lambda a, b, reg: reg[a] | b,
    'setr': lambda a, b, reg: reg[a],
    'seti': lambda a, b, reg: a,
    'gtir': lambda a, b, reg: int(a > reg[b]),
    'gtri': lambda a, b, reg: int(reg[a] > b),
    'gtrr': lambda a, b, reg: int(reg[a] > reg[b]),
    'eqir': lambda a, b, reg: int(a == reg[b]),
    'eqri': lambda a, b, reg: int(reg[a] == b),
    'eqrr': lambda a, b, reg: int(reg[a] == reg[b]),
}

def parse_insts(f):
    for line in f:
        opcode, operands = line[:-1].split(' ', 1)
        a, b, out = map(int, operands.split())
        yield opcode, a, b, out

line = sys.stdin.readline()[:-1]
ip = int(line[4:])
program = list(parse_insts(sys.stdin))

# part 1
reg = [0, 0, 0, 0, 0, 0]

while reg[ip] < len(program):
    opcode, a, b, out = program[reg[ip]]
    reg[out] = isa[opcode](a, b, reg)
    reg[ip] += 1

print(reg[0])

# part 2
reg = [1, 0, 0, 0, 0, 0]

while reg[ip] != 1:
    opcode, a, b, out = program[reg[ip]]
    reg[out] = isa[opcode](a, b, reg)
    reg[ip] += 1

n = reg[5]
print(sum(0 if n % reg1 else reg1 for reg1 in range(1, n + 1)))
