#!/usr/bin/env python3
import sys
from itertools import combinations, islice
from operator import add, mul, lt, eq

def run(p, get_input, memsize=0):
    def decode_param(offset):
        return p[pc + offset], modes // (10 ** (offset - 1)) % 10

    def pload(offset):
        param, mode = decode_param(offset)
        return param if mode == 1 else p[param + relbase * mode // 2]

    def pstore(offset, value):
        param, mode = decode_param(offset)
        p[param + relbase * mode // 2] = value

    opmap = {1: add, 2: mul, 7: lt, 8: eq}
    p = p + [0] * memsize
    pc = relbase = 0

    while p[pc] != 99:
        modes, opcode = divmod(p[pc], 100)

        if opcode in (1, 2, 7, 8):
            pstore(3, opmap[opcode](pload(1), pload(2)))
            pc += 4
        elif opcode == 3:
            pstore(1, get_input())
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

def read_grid(program):
    output = ''.join(map(chr, run(program, None, 10000)))
    lines = output.rstrip().split('\n')
    def gen_lines():
        yield '.' * len(lines[0])
        yield from lines
        yield '.' * len(lines[0])
    return [list('.%s.' % line) for line in gen_lines()]

def intersections(grid):
    for y, row in islice(enumerate(grid), 1, len(grid) - 1):
        for x, cell in islice(enumerate(row), 1, len(row) - 1):
            if row[x - 1:x + 2] == list('###') and \
                    grid[y - 1][x] == '#' and grid[y + 1][x] == '#':
                yield x, y

def calibrate(grid):
    return sum((x - 1) * (y - 1) for x, y in intersections(grid))

def find_path(grid):
    x, y = next((x, y) for y, row in enumerate(grid)
                for x, cell in enumerate(row) if cell in '^v<>')
    dx, dy = {'^': (0, -1), 'v': (0, 1), '<': (-1, 0), '>': (1, 0)}[grid[y][x]]
    turn = None

    while True:
        # walk forward
        forward = 0
        while grid[y + dy][x + dx] == '#':
            x += dx
            y += dy
            forward += 1

        if forward > 0:
            # when blocked, turn right
            if turn:
                yield turn
            yield str(forward)
            turn = 'R'
            dx, dy = -dy, dx
        elif turn == 'R':
            # if right is blocked, turn left instead
            turn = 'L'
            dx, dy = -dx, -dy
        elif turn is None:
            turn = 'R'
            dx, dy = -dy, dx
        else:
            # if left is blocked too, we're at the end
            break

def subroutines(path):
    for l in range(11, 1, -1):
        for i in range(len(path) - 2 * l):
            subseq = path[i:i + l]
            starts = [i]
            for j in range(i + l, len(path)):
                if path[j:j + l] == subseq:
                    starts.append(j)
            if len(starts) > 1:
                yield l, starts

def pick_subroutines(path):
    work = set()
    for l, starts in subroutines(path):
        for use in range(len(starts), 1, -1):
            for used_starts in combinations(starts, use):
                prio = -l * len(used_starts), -l
                work.add((prio, l, used_starts))

    # get rid of overlaps
    taken = [False] * len(path)
    for prio, l, starts in sorted(work):
        if any(any(taken[i:i + l]) for i in starts):
            continue
        for start in starts:
            for i in range(start, start + l):
                taken[i] = True
        start = starts[0]
        yield ','.join(path[start:start + l])

def make_subroutines(path):
    path = list(path)
    subs = {'A': '', 'B': '', 'C': ''}
    main = ','.join(path)
    for name, sub in zip('ABC', islice(pick_subroutines(path), 3)):
        subs[name] = sub
        main = main.replace(sub, name)
    assert len(main) <= 20
    assert all(len(sub) <= 20 for sub in subs.values())
    return main, subs

def rescue(program, main, subs, gridlen):
    lines = [main, subs['A'], subs['B'], subs['C'], 'n']
    inputs = list(map(ord, ('\n'.join(lines) + '\n')[::-1]))
    for output in run(program, inputs.pop, 10000):
        pass
    return output

# part 1
program = list(map(int, sys.stdin.readline().split(',')))
grid = read_grid(program)
print(calibrate(grid))

# part 2
path = list(find_path(grid))
program[0] = 2
main, subs = make_subroutines(path)
print(rescue(program, main, subs, len(grid) * len(grid[0])))
