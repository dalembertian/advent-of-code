#!/usr/bin/env python
# encoding: utf-8

import argparse


def main(args):
    line = read_lines(args.filename)
    filesystem = expand(line)
    compact(filesystem)

    print(f'Part 1 - Checksum of filesystem is: {checksum(filesystem)}')

def checksum(filesystem):
    return sum(i * j for i, j in enumerate(filesystem))

def compact(filesystem):
    try:
        while True:
            pos = filesystem.index(-1)
            filesystem[pos] = filesystem.pop()
    except:
        pass

def expand(line):
    filesystem = []
    is_block, ID = True, 0
    for c in line:
        n = int(c)
        if is_block:
            filesystem.extend([ID for i in range(n)])
            is_block, ID = False, ID+1
        else:
            filesystem.extend([-1 for i in range(n)])
            is_block = True
    return filesystem

def read_lines(filename):
    with open(filename) as lines:
        return lines.readline().strip()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
