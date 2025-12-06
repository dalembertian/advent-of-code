#!/usr/bin/env python
# encoding: utf-8

import argparse
import re

from functools import reduce


def main(args):
    lines, operators = read_lines(args.filename)
    
    # Correct: 5782351442566
    print(f'Part 1 - total: {compute_operations(operands_per_line(lines), operators)}')

    # Correct: 10194584711842
    print(f'Part 2 - total: {compute_operations(operands_per_column(lines), operators)}')


def compute_operations(operands, operators):
    total = 0
    for i in range(len(operators)):
        if operators[i] == '+':
            ops = [0 if o[i] == -1 else o[i] for o in operands]
            total += reduce(lambda x, y: x + y, ops)
        else:
            ops = [1 if o[i] == -1 else o[i] for o in operands]
            total += reduce(lambda x, y: x * y, ops)
    return total


def operands_per_column(lines):
    # Assuming no operand is bigger than <number of lines> digits
    width = len(lines[0])
    amount = len(lines)
    empty = ' ' * amount
    eol = '\n' * amount
    operands = [[] for _ in range(amount)]
    j = 0
    for i in range(width):
        number = ''.join([line[i] for line in lines])
        if number == empty or number == eol:
            # Not all operands might be present, so marking that case with -1
            for k in range(j, amount):
                operands[k].append(-1)
            j = 0
        else:
            operands[j].append(int(number))
            j += 1
    return operands


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
