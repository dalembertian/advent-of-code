#!/usr/bin/env python
# encoding: utf-8

from argparse import ArgumentParser
from functools import cache

DESIGNS = []

def main(args):
    patterns = read_lines(args.filename)
    ways = [search_for_pattern(0, pattern) for pattern in patterns]

    print(f'Part 1 - possible patterns: {len([w for w in ways if w > 0])}')
    print(f'Part 2 - different ways to make patterns: {sum(ways)}')

@cache
def search_for_pattern(start, pattern):
    if start == len(pattern):
        return 1
    ways = 0
    for design, length in DESIGNS:
        if pattern[start:start+length] == design:
            ways += search_for_pattern(start + length, pattern)
    return ways

def read_lines(filename):
    with open(filename) as input:
        designs = [(d.strip(), len(d.strip())) for d in input.readline().strip().split(',')]
        input.readline()
        patterns = [line.strip() for line in input.readlines()]
    DESIGNS.extend(designs)
    return patterns

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
