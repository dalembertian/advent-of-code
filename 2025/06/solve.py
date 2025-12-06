#!/usr/bin/env python
# encoding: utf-8

import argparse
import re

from functools import reduce


def main(args):
    operands, operators = read_lines(args.filename)
    
    for operand in operands:
        print(operand)
    print(operators)

    total = 0
    for i in range(len(operators)):
        if operators[i] == '+':
            total += reduce(lambda x, y: x + y, [o[i] for o in operands])
        else:
            total += reduce(lambda x, y: x * y, [o[i] for o in operands])

    # Correct:   5782351442566
    print(f'Part 1 - total: {total}')


def read_lines(filename):
    valid = re.compile(r'[\d\+\*]+')
    elements = []
    with open(filename) as lines:
        for line in lines:
            elements.append(re.findall(valid, line))
    operators = elements.pop()
    operands = [[int(e) for e in line] for line in elements]
    return operands, operators


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
