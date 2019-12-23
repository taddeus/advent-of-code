from operator import add, mul, lt, eq

def read_program(f):
    return list(map(int, f.readline().split(',')))

def run(p):
    def decode_param(offset):
        return p[pc + offset], modes // (10 ** (offset - 1)) % 10

    def address(param, mode):
        addr = param + relbase * mode // 2
        if addr >= len(p):
            p.extend([0] * (addr - len(p) + 1))
        return addr

    def pload(offset):
        param, mode = decode_param(offset)
        return param if mode == 1 else p[address(param, mode)]

    def pstore(offset, value):
        param, mode = decode_param(offset)
        p[address(param, mode)] = value

    opmap = {1: add, 2: mul, 7: lt, 8: eq}
    p = list(p)
    pc = relbase = 0

    while p[pc] != 99:
        modes, opcode = divmod(p[pc], 100)

        if opcode in (1, 2, 7, 8):
            pstore(3, opmap[opcode](pload(1), pload(2)))
            pc += 4
        elif opcode == 3:
            pstore(1, (yield))
            pc += 2
        elif opcode == 4:
            yield pload(1)
            pc += 2
        elif opcode == 5:
            pc = pload(2) if pload(1) else pc + 3
        elif opcode == 6:
            pc = pload(2) if not pload(1) else pc + 3
        elif opcode == 9:
            relbase += pload(1)
            pc += 2

def run_inputs(p, inputs):
    inputs = iter(inputs)
    computer = run(p)
    for outp in computer:
        while outp is None:
            outp = computer.send(next(inputs))
        yield outp

def run_getter(p, get_input):
    def gen_inputs():
        while True:
            yield get_input()
    return run_inputs(p, gen_inputs())
