#!/usr/bin/env python3
def lowest_house_nr(threshold, npres, nvisit):
    houses = [npres]

    while True:
        prevlen = len(houses)
        houses += [0] * prevlen
        limit = len(houses) + 1

        for elf in range(1, limit):
            start = prevlen + elf - prevlen % elf
            visited = prevlen // elf

            for house in range(start, limit, elf):
                if visited >= nvisit:
                    break
                houses[house - 1] += elf * npres
                visited += 1

        for i, val in enumerate(houses[prevlen:]):
            if val >= threshold:
                return prevlen + i + 1

print(lowest_house_nr(36000000, 10, 10000000))
print(lowest_house_nr(36000000, 11, 50))
