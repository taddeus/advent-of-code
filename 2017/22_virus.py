#!/usr/bin/env python3
import sys


class PartOne:
    def __init__(self, grid):
        self.infected = set()
        for y, line in enumerate(grid.split('\n')):
            for x, cell in enumerate(line):
                if cell == '#':
                    self.infected.add((y, x))
        self.y = y // 2
        self.x = x // 2
        self.dy = -1
        self.dx = 0

    def turn_left(self):
        self.dy, self.dx = -self.dx, self.dy

    def turn_right(self):
        self.dy, self.dx = self.dx, -self.dy

    def advance(self):
        pos = self.y, self.x
        if pos in self.infected:
            self.infected.remove(pos)
            self.turn_right()
            infection = False
        else:
            self.infected.add(pos)
            self.turn_left()
            infection = True

        self.y += self.dy
        self.x += self.dx
        return infection


CLEAN, FLAGGED, INFECTED, WEAKENED = range(4)


class PartTwo(PartOne):
    def __init__(self, grid):
        self.nodes = {}
        for y, line in enumerate(grid.split('\n')):
            for x, cell in enumerate(line):
                if cell == '#':
                    self.nodes[(y, x)] = INFECTED
        self.y = y // 2
        self.x = x // 2
        self.dy = -1
        self.dx = 0

    def at(self, y, x):
        return self.nodes.get((y, x), CLEAN)

    def turn_back(self):
        self.dy, self.dx = -self.dy, -self.dx

    def advance(self):
        state = self.at(self.y, self.x)

        if state == CLEAN:
            self.turn_left()
        elif state == INFECTED:
            self.turn_right()
        elif state == FLAGGED:
            self.turn_back()

        self.nodes[(self.y, self.x)] = (self.at(self.y, self.x) + 3) % 4

        self.y += self.dy
        self.x += self.dx
        return state == WEAKENED


grid = sys.stdin.read().rstrip()

state = PartOne(grid)
print(sum(int(state.advance()) for i in range(10000)))

state = PartTwo(grid)
print(sum(int(state.advance()) for i in range(10000000)))
