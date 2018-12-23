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

def run():
    reg = [0, 0, 0, 0, 0, 0]
    while reg[ip] < len(program):
        opcode, a, b, out = program[reg[ip]]
        reg[out] = isa[opcode](a, b, reg)
        reg[ip] += 1

        if reg[ip] == 28:
            yield reg[4]
        elif reg[ip] == 17:
            reg[3] //= 256
            reg[ip] = 8

def simulate():
    #r0 = 0
    r3 = r4 = 0
    while True:
        r3 = r4 | 65536
        r4 = 4332021

        while True:
            r4 = (((r4 + (r3 & 255)) & 16777215) * 65899) & 16777215

            if 256 > r3:
                break

            # program does this loop to divide r3 by 256:
            #r2 = 0
            #while (r2 + 1) * 256 <= r3:
            #    r2 += 1
            #r3 = r2

            r3 //= 256

        #if r4 == r0:
        #    break

        yield r4

line = sys.stdin.readline()[:-1]
ip = int(line[4:])
program = list(parse_insts(sys.stdin))
#numbers = run()
numbers = simulate()

# part 1
first = next(numbers)
print(first)

# part 2
seen = set()
last = first
for n in numbers:
    if n in seen:
        break
    seen.add(n)
    last = n
print(last)
