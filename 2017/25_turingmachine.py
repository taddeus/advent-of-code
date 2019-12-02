#!/usr/bin/env python3
import sys


class TuringMachine:
    def __init__(self, f):
        def last_word(linenr):
            return lines[linenr].split()[-1][:-1]

        def state_index(state):
            return (ord(state) - ord('A')) * 2

        def transition(start):
            write_val = int(last_word(start))
            move = 1 if last_word(start + 1) == 'left' else -1
            next_state = state_index(last_word(start + 2))
            return write_val, move, next_state

        lines = f.read().split('\n')
        self.state = state_index(last_word(0))
        self.steps = int(lines[1].split()[-2])
        self.trans = []
        self.tape = 0
        self.index = 0

        for start in range(3, len(lines), 10):
            in_state = state_index(last_word(start))
            assert in_state == len(self.trans)
            self.trans.append(transition(start + 2))
            self.trans.append(transition(start + 6))

    def step(self):
        read_val = (self.tape >> self.index) & 1
        write_val, move, next_state = self.trans[self.state + read_val]

        if write_val != read_val:
            mask = 1 << self.index
            if write_val:
                self.tape |= mask
            else:
                self.tape &= ~mask

        self.index += move
        if self.index == -1:
            self.tape <<= 1
            self.index = 0

        self.state = next_state
        self.steps -= 1

    def diag(self):
        while self.steps > 0:
            self.step()
        checksum = 0
        tape = self.tape
        while tape > 0:
            checksum += tape & 1
            tape >>= 1
        return checksum


print(TuringMachine(sys.stdin).diag())
