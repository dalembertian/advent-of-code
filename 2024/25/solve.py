#!/usr/bin/env python
# encoding: utf-8

import argparse
import re

from functools import reduce

def main(args):
    locks, keys = read_lines(args.filename)

    K = key_sizes(keys)
    fittings = [reduce(lambda a,b: a & b, [K[pin][5-space] for pin, space in enumerate(lock)]) for lock in locks]
    print(f'Part 1 - lock/key combinations is: {sum(len(f) for f in fittings)}')

def key_sizes(keys):
    # K[pin][max pin size]
    K = [[set() for j in range(6)] for i in range(5)]
    for n, key in enumerate(keys):
        for pin, size in enumerate(key):
            for max_size in range(5, size-1, -1):
                K[pin][max_size].add(n)
    return K

def read_lines(filename):
    lock = re.compile(r'(#+)(\.+)')
    key  = re.compile(r'(\.+)(#+)')
    locks = []
    keys = []
    with open(filename) as input:
        lines = input.readlines()
    for i in range(0, len(lines), 8):
        piece = [line.strip() for line in lines[i:i+7]]
        sided = [''.join([line[i] for line in piece]) for i in range(5)]
        if sided[0][0] == '#':
            locks.append([len(lock.search(pin).group(1))-1 for pin in sided])
        else:
            keys.append([len(key.search(pin).group(2))-1 for pin in sided])
    return locks, keys

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
