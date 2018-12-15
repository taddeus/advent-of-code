#!/usr/bin/env python3
import sys
from operator import attrgetter
from collections import defaultdict

SPACE, WALL = 0, 1

class BattleLost(Exception):
    def __init__(self, team):
        self.team = team

class Unit:
    counts = defaultdict(int)

    def __init__(self, pos, team, ap):
        self.pos = pos
        self.team = team
        self.hp = 200
        self.ap = ap
        self.counts[team] += 1

    def neighbouring_enemies(self):
        for nb in (self.pos - w, self.pos - 1, self.pos + 1, self.pos + w):
            u = grid[nb]
            if u not in (SPACE, WALL) and u.team != self.team and u.hp > 0:
                yield u

    def hit(self, ap):
        self.hp -= ap
        if self.hp <= 0:
            grid[self.pos] = SPACE

            self.counts[self.team] -= 1
            if self.counts[self.team] == 0:
                raise BattleLost(self.team)

    def fight(self):
        enemies = list(self.neighbouring_enemies())
        if enemies:
            min(enemies, key=attrgetter('hp', 'pos')).hit(self.ap)
        return len(enemies) > 0

    def move(self):
        step = self.step_to_nearest_enemy()
        if step is None:
            return False
        grid[self.pos] = SPACE
        grid[step] = self
        self.pos = step
        return True

    def step_to_nearest_enemy(self):
        source = self.pos
        Q = set(i for i, cell in enumerate(grid) if cell == SPACE)
        Q.add(source)
        size = max(Q) + 1
        inf = len(grid) + 1
        dist = [inf] * size
        dist[source] = 0
        prev = [None] * size

        while Q:
            u = min(Q, key=lambda x: (dist[x], x))
            Q.remove(u)
            for v in (u - w, u - 1, u + 1, u + w):
                if v in Q:
                    alt = dist[u] + 1
                    if alt < dist[v]:
                        dist[v] = alt
                        prev[v] = u

        def adjacent_enemies(v):
            if dist[v] < inf and grid[v] == SPACE:
                for nb in (v - w, v - 1, v + 1, v + w):
                    u = grid[nb]
                    if u not in (WALL, SPACE) and u.team != self.team and u.hp > 0:
                        yield u

        shortest = {}
        for v, d in enumerate(dist):
            for u in adjacent_enemies(v):
                step = v
                pathlen = 1
                while prev[step] != source:
                    step = prev[step]
                    pathlen += 1
                entry = pathlen, v, step
                if u not in shortest or entry < shortest[u]:
                    shortest[u] = entry

        if len(shortest):
            return min(shortest.values())[-1]

def parse(f):
    grid = []
    w = 0
    for y, line in enumerate(f):
        for x, c in enumerate(line.rstrip()):
            if c == '#':
                grid.append(WALL)
            elif c in '.':
                grid.append(SPACE)
            else:
                grid.append(Unit(y * w + x, c, 3))
        w = x + 1
    return grid, w

def show():
    def red(text):
        return '\x1b[31m' + text + '\x1b[0m'
    def green(text):
        return '\x1b[32m' + text + '\x1b[0m'

    h = len(grid) // w
    for y in range(h):
        line = ''
        hps = []
        for x in range(w):
            cell = grid[y * w + x]
            if cell not in (WALL, SPACE):
                color = red if cell.team == 'G' else green
                t = color(cell.team)
                hps.append('%s(%d)' % (t, cell.hp))
                line += t
            else:
                line += '#' if cell == WALL else ' '
        if hps:
            line += '   ' + ', '.join(hps)
        print(line)

def simulate(ap):
    global units
    rounds = 0
    clear = '\033c'
    try:
        print(clear + 'after 0 rounds with', ap, 'ap:')
        show()
        while True:
            for unit in units:
                if unit.hp > 0 and not unit.fight() and unit.move():
                    unit.fight()
            units = sorted((u for u in units if u.hp > 0), key=attrgetter('pos'))
            rounds += 1
            print(clear + 'after', rounds, 'rounds with', ap, 'ap:')
            show()
    except BattleLost as lost:
        print(clear + 'after', rounds, 'rounds with', ap, 'ap:')
        show()
        winner = 'Goblins' if lost.team == 'E' else 'Elves'
        return winner, rounds, sum(u.hp for u in units if u.hp > 0)

def reset(elf_ap):
    Unit.counts.clear()
    grid = []
    units = []
    for i, cell in enumerate(startgrid):
        if cell in (SPACE, WALL):
            grid.append(cell)
        else:
            unit = Unit(i, cell.team, elf_ap if cell.team == 'E' else 3)
            grid.append(unit)
            units.append(unit)
    return grid, units

elf_ap = 3
startgrid, w = parse(sys.stdin)
grid, units = reset(elf_ap)
startelves = sum(1 for u in units if u.team == 'E')

# part 1
winner, rounds, hp = simulate(elf_ap)
print('Combat ends after', rounds, 'full rounds:')
print(winner, 'win with', hp, 'hit points left')
print('Outcome:', rounds, '*', hp, '=', rounds * hp)

# part 2
numelves = 0
while winner != 'Elves' or numelves != startelves:
    elf_ap += 1
    grid, units = reset(elf_ap)
    winner, rounds, hp = simulate(elf_ap)
    numelves = sum(1 for u in units if u.team == 'E')

print('Elves need', elf_ap, 'attack power not to let any elf die')
print('Combat ends after', rounds, 'full rounds:')
print(winner, 'win with', hp, 'hit points left')
print('Outcome:', rounds, '*', hp, '=', rounds * hp)
