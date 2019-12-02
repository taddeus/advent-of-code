#!/usr/bin/env python3
import sys


class Screen:
    def __init__(self, width, height):
        self.rows = [[False] * width for y in range(height)]

    def fill_rect(self, width, height):
        for y in range(height):
            for x in range(width):
                self.rows[y][x] = True

    def rotate_row(self, row, amount):
        self.rows[row][:] = self.rows[row][-amount:] + self.rows[row][:-amount]

    def rotate_col(self, col, amount):
        old = [row[col] for row in self.rows]
        for y, row in enumerate(self.rows):
            row[col] = old[y - amount]

    def count_on(self):
        return sum(sum(map(int, row)) for row in self.rows)

    def process(self, f):
        for line in f:
            words = line.split()
            if words[0] == 'rect':
                a, b = words[1].split('x')
                self.fill_rect(int(a), int(b))
            else:
                assert words[0] == 'rotate'
                fn = self.rotate_row if words[1] == 'row' else self.rotate_col
                fn(int(words[2][2:]), int(words[4]))

    def print(self):
        for row in self.rows:
            print(''.join('#' if px else '.' for px in row))


screen = Screen(50, 6)
screen.process(sys.stdin)
print(screen.count_on(), 'pixels on:')
screen.print()
