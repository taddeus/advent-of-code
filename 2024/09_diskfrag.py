#!/usr/bin/env python3
import sys

def parse(digits):
    files = []
    free = []
    is_file = True
    pos = 0
    for size in map(int, digits):
        if is_file:
            files.append((len(files), pos, size))
        else:
            free.append((pos, size))
        pos += size
        is_file = not is_file
    return files, free

def move_blocks(free, files):
    fid = len(files) - 1
    for i, (free_pos, free_size) in enumerate(free):
        while free_size:
            _, pos, size = files[fid]
            if pos < free_pos:
                return checksum(files)
            moved = min(size, free_size)
            files.append((fid, free_pos, moved))
            files[fid] = fid, pos, size - moved
            free_pos += moved
            free_size -= moved
            fid -= moved == size

def move_files(free, files):
    for fid, pos, size in reversed(files):
        for i, (free_pos, free_size) in enumerate(free):
            if free_pos > pos:
                break
            if free_size >= size:
                files[fid] = fid, free_pos, size
                free[i] = free_pos + size, free_size - size
                break
    return checksum(files)

def checksum(files):
    return sum((pos + i) * fid for fid, pos, size in files for i in range(size))

files, free = parse(sys.stdin.read().rstrip())
print(move_blocks(free, list(files)))
print(move_files(free, files))
