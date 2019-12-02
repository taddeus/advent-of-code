#!/usr/bin/env python3
import sys
from operator import add, mul

def run(p):
    pc = 0
    while p[pc] != 99:
        opcode, in1, in2, out = p[pc:pc + 4]
        op = add if opcode == 1 else mul
        p[out] = op(p[in1], p[in2])
        pc += 4

def initrun(p, noun, verb):
    p = list(p)
    p[1:3] = noun, verb
    run(p)
    return p[0]

def find_params(p, desired_result):
    noun = verb = 0
    while initrun(p, noun, verb) <= desired_result:
        noun += 1
    noun -= 1
    while initrun(p, noun, verb) < desired_result:
        verb += 1
    return 100 * noun + verb

program = list(map(int, sys.stdin.read().split(',')))
print(initrun(program, 12, 2))
print(find_params(program, 19690720))
