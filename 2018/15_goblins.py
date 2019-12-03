#!/usr/bin/env python3
import sys
from operator import attrgetter
from heapq import heappush, heappop

SPACE, WALL = 0, 1
GOBLINS, ELVES = 0, 1

class Unit:
    counts = [0, 0]

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
        dist = {source: 0}
        prev = {}
        Q = [(0, source)]
        visited = {source}

        while Q:
            udist, u = heappop(Q)
            for v in (u - w, u - 1, u + 1, u + w):
                if grid[v] == SPACE and v not in visited:
                    visited.add(v)
                    alt = udist + 1
                    known = dist.get(v, None)
                    if known is None or alt < known:
                        dist[v] = alt
                        prev[v] = u
                        heappush(Q, (alt, v))

        def adjacent_enemies(v):
            if v in dist and grid[v] == SPACE:
                for nb in (v - w, v - 1, v + 1, v + w):
                    u = grid[nb]
                    if u not in (WALL, SPACE) and u.team != self.team and u.hp > 0:
                        yield u

        shortest = {}
        for v, d in dist.items():
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

class BattleLost(Exception):
    def __init__(self, team):
        self.team = team

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
                grid.append(Unit(y * w + x, ELVES if c == 'E' else GOBLINS, 3))
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
                t = green('E') if cell.team == ELVES else red('G')
                hps.append('%s(%d)' % (t, cell.hp))
                line += t
            else:
                line += '#' if cell == WALL else ' '
        if hps:
            line += '   ' + ', '.join(hps)
        print(line)

def simulate(ap, verbose):
    global units
    rounds = 0
    clear = '\033c'
    try:
        if verbose:
            print(clear + 'after 0 rounds with', ap, 'ap:')
            show()
        while True:
            for unit in units:
                if unit.hp > 0 and not unit.fight() and unit.move():
                    unit.fight()
            units = sorted((u for u in units if u.hp > 0), key=attrgetter('pos'))
            rounds += 1
            if verbose:
                print(clear + 'after', rounds, 'rounds with', ap, 'ap:')
                show()
    except BattleLost as lost:
        if verbose:
            print(clear + 'after', rounds, 'rounds with', ap, 'ap:')
            show()
        return lost.team, rounds, sum(u.hp for u in units if u.hp > 0)

def reset(elf_ap):
    Unit.counts = [0, 0]
    grid = []
    units = []
    for i, cell in enumerate(startgrid):
        if cell in (SPACE, WALL):
            grid.append(cell)
        else:
            unit = Unit(i, cell.team, elf_ap if cell.team == ELVES else 3)
            grid.append(unit)
            units.append(unit)
    return grid, units

def report(loser, rounds, hp, ap):
    print('Combat ends after', rounds, 'full rounds with', ap, 'attack power:')
    winner = 'Goblins' if loser == ELVES else 'Elves'
    print(winner, 'win with', hp, 'hit points left')
    print('Outcome:', rounds, '*', hp, '=', rounds * hp)

# part 1
elf_ap = 3
verbose = len(sys.argv) == 2 and sys.argv[-1] == '-v'
startgrid, w = parse(sys.stdin)
grid, units = reset(elf_ap)
startelves = sum(1 for u in units if u.team == ELVES)
outcome = outcome3 = simulate(elf_ap, verbose)

# part 2
numelves = 0
while numelves != startelves:
    elf_ap += 1
    grid, units = reset(elf_ap)
    outcome = simulate(elf_ap, verbose)
    numelves = sum(1 for u in units if u.team == ELVES)

report(*outcome3, 3)
print()
print('Elves need', elf_ap, 'attack power not to let any elf die:')
report(*outcome, elf_ap)
