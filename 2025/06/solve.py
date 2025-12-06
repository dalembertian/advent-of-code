#!/usr/bin/env python
# encoding: utf-8

import argparse
import re

from functools import reduce


def main(args):
    lines, operators = read_lines(args.filename)
    
    # Correct:   5782351442566
    print(f'Part 1 - total: {compute_operations(operands_per_line(lines), operators)}')


def compute_operations(operands, operators):
    total = 0
    for i in range(len(operators)):
        if operators[i] == '+':
            total += reduce(lambda x, y: x + y, [o[i] for o in operands])
        else:
            total += reduce(lambda x, y: x * y, [o[i] for o in operands])
    return total


def operands_per_line(lines):
    valid = re.compile(r'[\d]+')
    return [[int(e) for e in re.findall(valid, line)] for line in lines]


def read_lines(filename):
    valid = re.compile(r'[\+\*]+')
    elements = []
    with open(filename) as lines:
        lines = lines.readlines()
    operators = re.findall(valid, lines.pop())
    return lines, operators


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
