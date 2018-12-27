#!/usr/bin/env python3
import sys
import re
from operator import attrgetter

class Units:
    def __init__(self, team, n, hp, dmg, dmgty, initiative, immune=[], weak=[]):
        self.team = team
        self.n = n
        self.hp = hp
        self.dmg = dmg
        self.dmgty = dmgty
        self.initiative = initiative
        self.immune = immune
        self.weak = weak

    def copy(self):
        return self.__class__(self.team, self.n, self.hp, self.dmg,
                self.dmgty, self.initiative, [i for i in self.immune],
                [w for w in self.weak])

    @classmethod
    def parse(cls, line, team):
        pat = r'(\d+) units each with (\d+) hit points (?:\(([^)]*)\) )?' \
              r'with an attack that does (\d+) (\w+) damage at initiative (\d+)'
        n, hp, special, dmg, dmgty, init = re.match(pat, line).groups()
        group = cls(team, int(n), int(hp), int(dmg), dmgty, int(init))
        if special:
            for spec in special.split('; '):
                ty, rest = spec.split(' to ')
                setattr(group, ty, rest.split(', '))
        return group

    def effective_power(self):
        return self.n * self.dmg

    def alive(self):
        return self.n > 0

    def pick_order(self):
        return self.effective_power(), self.initiative

    def damage_to(self, other):
        if self.dmgty in other.immune:
            return 0
        if self.dmgty in other.weak:
            return self.effective_power() * 2
        return self.effective_power()

    def attack(self, defender):
        nkilled = min(defender.n, self.damage_to(defender) // defender.hp)
        defender.n -= nkilled
        return nkilled

def parse(f):
    team = re.match(r'(.+):', f.readline()).group(1)
    for line in sys.stdin:
        line = line.rstrip()
        if line.endswith(':'):
            team = line[:-1]
        elif line:
            yield Units.parse(line, team)

def fight(groups):
    # target selection phase
    groups.sort(key=Units.pick_order, reverse=True)
    chosen = [False] * len(groups)
    picks = {}

    for attacker in groups:
        opts = []
        for i, defender in enumerate(groups):
            if defender.team != attacker.team and not chosen[i]:
                damage = attacker.damage_to(defender)
                if damage:
                    opts.append((damage, defender.effective_power(), defender.initiative, i))
        if opts:
            target = max(opts)[-1]
            if not chosen[target]:
                chosen[target] = True
                picks[attacker] = groups[target]

    # attack phase
    groups.sort(key=attrgetter('initiative'), reverse=True)

    progress = False
    for attacker in groups:
        if attacker.alive() and attacker in picks:
            progress |= attacker.attack(picks[attacker]) > 0

    return progress, [g for g in groups if g.alive()]

def simulate(initial, boost):
    groups = [g.copy() for g in initial]
    for g in groups:
        if g.team == 'Immune System':
            g.dmg += boost

    while len(set(u.team for u in groups)) > 1:
        progress, groups = fight(groups)
        if not progress:
            return 'Infection', 0

    return groups[0].team, sum(g.n for g in groups)

initial = list(parse(sys.stdin))

# part 1
winner, units = simulate(initial, 0)
assert winner == 'Infection'
print(units)

# part 2
boost = 0
while winner != 'Immune System':
    boost += 1
    winner, units = simulate(initial, boost)
print(units)
