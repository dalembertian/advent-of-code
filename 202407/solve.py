#!/usr/bin/env python
# encoding: utf-8

import argparse


def main(args):
    equations = read_lines(args.filename)

    # Part 1
    values = [(value, check_value(value, operands[:])) for value, operands in equations.items()]
    valids = [value[0] for value in values if value[1]]
    print(f'Part 1 - {len(valids)} valid equations, adding to {sum(valids)} valid values')

    # Part 2
    invalids = [value[0] for value in values if not value[1]]
    values   = [(value, check_value(value, equations[value][:], True)) for value in invalids]
    revalids = [value[0] for value in values if value[1]]
    print(f'Part 2 - {len(revalids)} REvalidATED equations, adding to {sum(revalids)} values, and total of {sum(valids)+sum(revalids)}')

def read_lines(filename):
    equations = {}
    with open(filename) as lines:
        for line in lines:
            k, v = line.strip().split(':')
            equations[int(k)] = [int(i) for i in v.split()]
    return equations

def check_value(value, operands, concat=False):
    if len(operands) == 1:
        return value == operands[0]
    else:
        op = operands.pop()
        m = check_value(value // op, operands[:], concat) if value % op == 0 else False
        a = check_value(value -  op, operands[:], concat) if value - op > 0  else False
        c = check_value(unconcat(value, op), operands[:], concat) if (concat and is_concat(value, op)) else False
        return m or a or c

def is_concat(value, ending):
    return value > 9 and str(value).endswith(str(ending))

def unconcat(value, ending):
    v = str(value)
    return int(v[:len(v)-len(str(ending))])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
