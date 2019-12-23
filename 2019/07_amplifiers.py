#!/usr/bin/env python3
import sys
from itertools import permutations
from intcode import read_program, run

def amplify(p, phases):
    amps = []
    signal = 0
    for phase in phases:
        amp = run(p)
        assert next(amp) is None
        assert amp.send(phase) is None
        signal = amp.send(signal)
        amps.append(amp)
    try:
        while True:
            for amp in amps:
                assert next(amp) is None
                signal = amp.send(signal)
    except StopIteration:
        return signal

program = read_program(sys.stdin)
print(max(amplify(program, phases) for phases in permutations(range(5))))
print(max(amplify(program, phases) for phases in permutations(range(5, 10))))
