#!/usr/bin/env python3
import sys
from ast import literal_eval
from functools import reduce
from itertools import permutations

class Number:
    def __init__(self, value, left, right):
        self.prev = self.next = None
        self.value = value
        self.left = left
        self.right = right

    @classmethod
    def maybe_pair(cls, maybe_list):
        if isinstance(maybe_list, int):
            return cls(maybe_list, None, None)
        left, right = map(cls.maybe_pair, maybe_list)
        return cls(None, left, right)

    @classmethod
    def fromlist(cls, list_num):
        root = cls.maybe_pair(list_num)
        prev = None
        for node in root.numbers():
            if prev:
                prev.next = node
            node.prev = prev
            prev = node
        return root

    def isnum(self):
        return self.value is not None

    def numbers(self):
        if self.isnum():
            yield self
        else:
            yield from self.left.numbers()
            yield from self.right.numbers()

    def __repr__(self):
        if self.value is not None:
            return repr(self.value)
        return '[%s,%s]' % (self.left, self.right)

    def first(self):
        return self if self.isnum() else self.left.first()

    def last(self):
        return self if self.isnum() else self.right.last()

    def add(self, other):
        new = self.__class__(None, self, other)
        l = self.last()
        r = other.first()
        l.next = r
        r.prev = l
        new.reduce()
        return new

    def explode(self, depth):
        if self.isnum():
            return False

        if self.left.isnum() and self.right.isnum() and depth >= 4:
            self.prev = self.left.prev
            self.next = self.right.next
            if self.left.prev:
                self.left.prev.value += self.left.value
                self.left.prev.next = self
            if self.right.next:
                self.right.next.value += self.right.value
                self.right.next.prev = self
            self.left = self.right = None
            self.value = 0
            return True

        return self.left.explode(depth + 1) or self.right.explode(depth + 1)

    def split(self):
        if not self.isnum():
            return self.left.split() or self.right.split()

        if self.value < 10:
            return False

        half, odd = divmod(self.value, 2)
        self.left = self.__class__(half, None, None)
        self.right = self.__class__(half + odd, None, None)
        if self.prev:
            self.prev.next = self.left
        if self.next:
            self.next.prev = self.right
        self.left.prev = self.prev
        self.left.next = self.right
        self.right.prev = self.left
        self.right.next = self.next
        self.value = self.prev = self.next = None
        return True

    def reduce(self):
        if not self.isnum() or self.split():
            if self.explode(0) or self.split():
                self.reduce()

    def magnitude(self):
        if self.isnum():
            return self.value
        return 3 * self.left.magnitude() + 2 * self.right.magnitude()

nums = list(map(literal_eval, sys.stdin))
print(reduce(Number.add, map(Number.fromlist, nums)).magnitude())
print(max(Number.fromlist(x).add(Number.fromlist(y)).magnitude()
          for x, y in permutations(nums, 2)))
