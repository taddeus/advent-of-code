#!/usr/bin/env python3
import sys
from intcode import read_program, run_iter

def run_nat(program):
    def boot(i):
        nic = run_iter(program, 100)
        assert next(nic) is None
        return nic

    nics, messages = zip(*[(boot(i), [i]) for i in range(50)])
    natpack = 0, 0

    while True:
        for i, (nic, msg) in enumerate(zip(nics, messages)):
            msg.append(-1)
            while msg:
                dst = nic.send(msg.pop(0))
                while dst is not None:
                    pack = next(nic), next(nic)
                    if dst == 255:
                        natpack = pack
                    else:
                        messages[dst].extend(pack)
                    dst = next(nic)

        if not any(messages):
            messages[0].extend(natpack)
            yield natpack[1]

def find_repeated_natpack(program):
    seen = set()
    for y in run_nat(program):
        if y in seen:
            return y
        seen.add(y)

program = read_program(sys.stdin)
print(next(run_nat(program)))
print(find_repeated_natpack(program))
