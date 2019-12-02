#!/usr/bin/env python3
from queue import PriorityQueue
from collections import namedtuple


Spell = namedtuple('Spell', 'cost duration damage heal armor mana'.split())
spells = [
    Spell(53,  0, 4, 0, 0, 0),
    Spell(73,  0, 2, 2, 0, 0),
    Spell(113, 6, 0, 0, 7, 0),
    Spell(173, 6, 3, 0, 0, 0),
    Spell(229, 5, 0, 0, 0, 101),
]


class State:
    def __init__(self, index, previous_cost, player_hp, player_mana,
                 boss_hp, boss_damage, hard, timers=None):
        self.index = index
        self.cost = previous_cost + spells[index].cost
        self.player_hp = player_hp
        self.player_mana = player_mana
        self.boss_hp = boss_hp
        self.boss_damage = boss_damage
        self.hard = hard
        self.timers = timers if timers else [0] * len(spells)

    def __lt__(self, other):
        return self.cost < other.cost

    def can_cast(self, index):
        return self.timers[index] <= 1 and \
               self.player_mana >= spells[index].cost

    def cast(self, index):
        spell = spells[index]
        self.player_mana -= spell.cost

        if spell.duration:
            self.timers[index] = spell.duration
        else:
            self.boss_hp -= spell.damage
            self.player_hp += spell.heal

    def apply_effects(self):
        for i, remain in enumerate(self.timers):
            if remain > 0:
                spell = spells[i]
                self.boss_hp -= spell.damage
                self.player_mana += spell.mana

                if remain == spell.duration:
                    self.boss_damage -= spell.armor
                elif remain == 1:
                    self.boss_damage += spell.armor

                self.timers[i] = remain - 1

    def turn(self, verbose=False):
        if self.hard:
            self.player_hp -= 1
            if self.player_hp <= 0:
                return
        self.apply_effects()
        self.cast(self.index)
        self.apply_effects()
        self.player_hp -= max(self.boss_damage, 1)

    def add_spell(self, index):
        return State(index, self.cost, self.player_hp, self.player_mana,
                     self.boss_hp, self.boss_damage, self.hard,
                     list(self.timers))


def min_win_cost(player_hp, player_mana, boss_hp, boss_damage, hard=False):
    worklist = PriorityQueue()
    indices = list(range(len(spells)))

    for index in indices:
        worklist.put(State(index, 0, player_hp, player_mana,
                           boss_hp, boss_damage, hard))

    while not worklist.empty():
        state = worklist.get()
        state.turn()

        if state.boss_hp <= 0:
            return state.cost

        if state.player_hp > 0:
            for index in indices:
                if state.can_cast(index):
                    worklist.put(state.add_spell(index))


assert min_win_cost(10, 250, 13, 8) == 226
assert min_win_cost(10, 250, 14, 8) == 641
print(min_win_cost(50, 500, 55, 8))
print(min_win_cost(50, 500, 55, 8, hard=True))
