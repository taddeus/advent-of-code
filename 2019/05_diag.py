#!/usr/bin/env python3
import sys
from intcode import read_program, run_inputs

program = read_program(sys.stdin)
print(list(run_inputs(program, [1]))[-1])
print(list(run_inputs(program, [5]))[-1])
