#!/usr/bin/env python3
import sys
from intcode import read_program, run_inputs

program = read_program(sys.stdin)
print(next(run_inputs(program, [1])))
print(next(run_inputs(program, [2])))
