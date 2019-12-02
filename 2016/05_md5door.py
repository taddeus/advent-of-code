#!/usr/bin/env python3
from hashlib import md5
from itertools import count


def hashes(key):
    for i in count(0):
        h = md5((key + str(i)).encode('ascii')).digest()
        if h[0] + h[1] == 0 and h[2] <= 0xf:
            yield h


def door1(key):
    password = ''

    for h in hashes(key):
        password += hex(h[2])[-1]
        if len(password) == 8:
            print('\r', end='')
            return password
        print('\r' + password, end='')


def door2(key):
    password = bytearray(b'\0\0\0\0\0\0\0\0')

    for h in hashes(key):
        i = h[2]
        if i < 8 and password[i] == 0:
            password[i] = ord('%x' % (h[3] >> 4))
            if all(password):
                print('\r', end='')
                return password.decode('ascii')
            print('\r' + password.decode('ascii').replace('\0', '_'), end='')


print(door1('ugkcyxxp'))
print(door2('ugkcyxxp'))
