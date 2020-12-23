#!/usr/bin/env python3
import sys

def parse(f):
    for line in f:
        opcode, arg = line.split()
        yield opcode, int(arg)

def run(program, acc=0):
    ip = 0
    seen = [False] * len(program)
    while ip < len(program):
        if seen[ip]:
            return False, acc
        seen[ip] = True
        opcode, arg = program[ip]
        if opcode == 'acc':
            acc += arg
        elif opcode == 'jmp':
            ip += arg - 1
        else:
            assert opcode == 'nop'
        ip += 1
    return True, acc

def patch(program):
    change = {'nop': 'jmp', 'jmp': 'nop'}
    for i, (opcode, arg) in enumerate(program):
        if opcode in change:
            program[i] = change[opcode], arg
            term, acc = run(program)
            if term:
                return acc
            program[i] = opcode, arg

program = list(parse(sys.stdin))
print(run(program)[1])
print(patch(program))
