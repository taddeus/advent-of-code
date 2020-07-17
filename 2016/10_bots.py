#!/usr/bin/env python3
import sys
from collections import defaultdict, deque


class Simulation:
    def __init__(self):
        self.bots = defaultdict(list)
        self.outputs = defaultdict(list)
        self.lows = {}
        self.highs = {}

    @classmethod
    def parse(cls, f):
        self = cls()
        dests = {'bot': self.bots, 'output': self.outputs}

        for line in f:
            words = line.split()
            if words[0] == 'value':
                self.bots[int(words[-1])].append(int(words[1]))
            else:
                bot = int(words[1])
                self.lows[bot] = dests[words[5]], int(words[6])
                self.highs[bot] = dests[words[-2]], int(words[-1])

        return self

    def run(self):
        queue = deque(bot for bot, ch in self.bots.items() if len(ch) == 2)
        self.comparisons = {}

        def give(dest, nr, chip):
            dest[nr].append(chip)
            if dest == self.bots and len(dest[nr]) == 2:
                queue.append(nr)

        while queue:
            bot = queue.popleft()
            chips = self.bots[bot]

            if len(chips) == 2:
                chips.sort()
                self.comparisons[tuple(chips)] = bot
                give(*self.highs[bot], chips.pop())
                give(*self.lows[bot], chips.pop())


sim = Simulation.parse(sys.stdin)
sim.run()
print(sim.comparisons[(17, 61)])
print(sim.outputs[0][0] * sim.outputs[1][0] * sim.outputs[2][0])
