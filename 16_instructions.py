#!/usr/bin/env python3
import sys
from collections import defaultdict

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

def run(exe, a, b, reg):
    reg = list(reg)
    reg[out] = exe(a, b, reg)
    return tuple(reg)

# part 1
effects, program = sys.stdin.read().rstrip().split('\n\n\n\n')
opcodes = [set(isa.keys()) for i in range(len(isa))]
three = 0

for effect in effects.split('\n\n'):
    before, inst, after = effect.split('\n')
    reg = tuple(map(int, before[9:-1].split(', ')))
    opcode, a, b, out = map(int, inst.split())
    expect = tuple(map(int, after[9:-1].split(', ')))
    mnems = set(mnem for mnem, exe in isa.items() if run(exe, a, b, reg) == expect)
    opcodes[opcode] &= mnems
    three += int(len(mnems) >= 3)

print(three)

# part 2
while sum(map(len, opcodes)) > len(isa):
    for opcode, mnems in enumerate(opcodes):
        if len(mnems) == 1:
            certain = next(iter(mnems))
            for other, mnems in enumerate(opcodes):
                if other != opcode:
                    mnems.discard(certain)
opcodes = [next(iter(mnems)) for mnems in opcodes]

reg = [0, 0, 0, 0]
for inst in program.split('\n'):
    opcode, a, b, out = map(int, inst.split())
    reg[out] = isa[opcodes[opcode]](a, b, reg)
print(reg[0])
