#!/usr/bin/env python3
import sys
from intcode import read_program, run

def run_springscript(program, script):
    inputs = list(map(ord, reversed(script)))
    interp = run(program, inputs.pop, 1000)
    return next(out for out in interp if out > 128)

# Jump if A or C is a hole and D is reachable:
# J = (!A | !C) & D
walkscript = '''
NOT A T
NOT C J
OR T J
AND D J
WALK
'''.lstrip()

# Jump if A is a hole, or B/C are holes and D is reachable, but we don't end up
# just before a hole at which we will have to jump but cannot:
# J = !A | (D & (!B | !C) & !(!E & !H))
#   = (!(B & C) & (E | H) & D) | !A
runscript = '''
OR B T
AND C T
NOT T J
NOT E T
NOT T T
OR H T
AND T J
AND D J
NOT A T
OR T J
RUN
'''.lstrip()

program = read_program(sys.stdin)
print(run_springscript(program, walkscript))
print(run_springscript(program, runscript))
