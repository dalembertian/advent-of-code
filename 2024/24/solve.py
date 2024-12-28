#!/usr/bin/env python
# encoding: utf-8

import argparse
import re

from collections import defaultdict

AND = lambda a, b: a & b
OR  = lambda a, b: a | b
XOR = lambda a, b: a ^ b
OPS = {
    'AND': AND,
    'OR': OR,
    'XOR': XOR
}

def main(args):
    depends, results, operats = read_lines(args.filename)
    print(depends)
    print(results)
    print(operats)

def read_lines(filename):
    initial = re.compile(r'(\w+): (\d+)')
    boolean = re.compile(r'(\w+) (AND|OR|XOR) (\w+) -> (\w+)')
    depends = defaultdict(list)
    results = {}
    operats = {}
    with open(filename) as lines:
        for line in lines:
            if initial.search(line):
                k, v = initial.search(line).groups()
                results[k] = int(v)
            if boolean.search(line):
                a, op, b, r = boolean.search(line).groups()
                depends[r].extend([a, b])
                operats[r] = (a, b, OPS[op])
    return depends, results, operats

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
