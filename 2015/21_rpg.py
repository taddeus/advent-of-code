#!/usr/bin/env python3
from collections import namedtuple
from itertools import combinations
from copy import copy


class Shop:
    Item = namedtuple('Item', ['cost', 'damage', 'armor'])
    weapons = [Item(  8, 4, 0), Item( 10, 5, 0), Item( 25, 6, 0),
               Item( 40, 7, 0), Item( 74, 8, 0)]
    armors = [Item( 13, 0, 1), Item( 31, 0, 2), Item( 53, 0, 3),
              Item( 75, 0, 4), Item(102, 0, 5)]
    rings = [Item( 25, 1, 0), Item( 50, 2, 0), Item(100, 3, 0),
             Item( 20, 0, 1), Item( 40, 0, 2), Item( 80, 0, 3)]

    @classmethod
    def item_combos(cls):
        for nrings in range(0, 3):
            for rings in map(list, combinations(cls.rings, nrings)):
                for weapon in cls.weapons:
                    yield [weapon] + rings
                    for armor in cls.armors:
                        yield [weapon, armor] + rings

    @classmethod
    def weighted_combos(cls):
        for items in cls.item_combos():
            yield sum(item.cost for item in items), items


class Player:
    def __init__(self, hp, damage, armor):
        self.hp = hp
        self.damage = damage
        self.armor = armor

    def attack(self, other):
        other.hp -= max(self.damage - other.armor, 1)

    def alive(self):
        return self.hp > 0

    def with_items(self, items):
        newme = copy(self)
        for item in items:
            newme.damage += item.damage
            newme.armor += item.armor
        return newme

    def fight(self, other):
        attacker = self
        defender = other
        while attacker.alive() and defender.alive():
            attacker.attack(defender)
            attacker, defender = defender, attacker
        return self.alive()


me = Player(100, 0, 0)
boss = Player(104, 8, 1)

# part 1
combos = sorted(Shop.weighted_combos())
for cost, items in combos:
    if me.with_items(items).fight(copy(boss)):
        print(cost)
        break

# part 2
for cost, items in reversed(combos):
    if not me.with_items(items).fight(copy(boss)):
        print(cost)
        break
