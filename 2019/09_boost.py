#!/usr/bin/env python3
import sys
from intcode import read_program, run

program = read_program(sys.stdin)
print(next(run(program, [1].pop, 10000)))
print(next(run(program, [2].pop, 10000)))
