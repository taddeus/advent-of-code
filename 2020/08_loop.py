#!/usr/bin/env python3
import sys

def parse(f):
    for line in f:
        opcode, arg = line.split()
        yield opcode, int(arg)

def run(program, acc=0):
    ip = 0
    yield ip, acc
    while ip < len(program):
        opcode, arg = program[ip]
        if opcode == 'acc':
            acc += arg
        elif opcode == 'jmp':
            ip += arg - 1
        else:
            assert opcode == 'nop'
        ip += 1
        yield ip, acc

def acc_after_one_iteration(program):
    seen = set()
    return next(acc for ip, acc in run(program) if ip in seen or seen.add(ip))

def mutate(program):
    change = {'nop': 'jmp', 'jmp': 'nop'}
    for i, (opcode, arg) in enumerate(program):
        if opcode != 'acc':
            program[i] = change[opcode], arg
            yield program
            program[i] = opcode, arg

def patch(program, maxn):
    for p in mutate(program):
        for n, (ip, acc) in zip(range(maxn), run(p)):
            pass
        if n < maxn - 1:
            return program

program = list(parse(sys.stdin))
print(acc_after_one_iteration(program))
for ip, acc in run(patch(program, 1000)):
    pass
print(acc)
