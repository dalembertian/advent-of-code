#!/usr/bin/env python
# encoding: utf-8

import argparse
import re
from collections import defaultdict
        
DIRECTIONS = ((-1, 0), (1, 0), (0, -1), (0, 1))

def main(args):
    machines = read_lines(args.filename)
    # print(machines)

    prizes = get_prizes(machines)
    print(f'Part 1 - Total amount of tokens to win {len(prizes)} prizes is: {sum(prizes)}')

def get_prizes(machines):
    prizes = []
    for a, b, prize in machines:
        factors = set(factor(prize[0], a[0], b[0]))
        factors = factors.intersection(factor(prize[1], a[1], b[1]))
        if factors:
            prizes.append(min([3*x + y for x, y in factors]))
    return prizes

def factor(number, a, b):
    factors = []
    i, factor = 0, 0
    while factor <= number:
        rest = number - factor
        if b <= rest and rest % b == 0:
            factors.append((i, rest // b))
        i, factor = i + 1, factor + a
    return factors

def read_lines(filename):
    values = re.compile(r'.*X[+|=](\d+), Y[+|=](\d+)')
    machines = []
    with open(filename) as input:
        lines = input.readlines()
    lines.insert(0, '')
    while lines:
        lines.pop(0)
        machines.append((
            tuple([int(e) for e in values.search(lines.pop(0)).groups()]),
            tuple([int(e) for e in values.search(lines.pop(0)).groups()]),
            tuple([int(e) for e in values.search(lines.pop(0)).groups()]),
        ))
    return machines

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
