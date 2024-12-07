#!/usr/bin/env python
# encoding: utf-8

import argparse


def main(args):
    equations = read_lines(args.filename)

    # Part 1
    values = [(value, check_value(value, operands[:])) for value, operands in equations.items()]
    valids = [value[0] for value in values if value[1]]
    print(f'Part 1 - {len(valids)} valid equations, adding to {sum(valids)} valid values')

def read_lines(filename):
    equations = {}
    with open(filename) as lines:
        for line in lines:
            k, v = line.strip().split(':')
            equations[int(k)] = [int(i) for i in v.split()]
    return equations

def check_value(value, operands):
    # print(value, operands)
    if len(operands) == 1:
        # print(value == operands[0])
        return value == operands[0]
    else:
        op = operands.pop()
        return (check_value(value // op, operands[:]) if value % op == 0 else False) or \
               (check_value(value -  op, operands[:]) if value - op > 0  else False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
