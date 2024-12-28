#!/usr/bin/env python
# encoding: utf-8

import argparse
import re

from collections import defaultdict

AND = lambda a, b: a & b
OR  = lambda a, b: a | b
XOR = lambda a, b: a ^ b
NUL = lambda a, b: a
OPS = {
    'AND': AND,
    'OR': OR,
    'XOR': XOR,
    'NUL': NUL,
}

def main(args):
    depends, is_deps, operats, results = read_lines(args.filename)
    all_nodes = set(depends.keys() | is_deps.keys())

    order = kahn(all_nodes - depends.keys(), is_deps, depends)
    calculate(operats, results, order)
    z_wires = sorted([(wire, output) for wire, output in results.items() if wire[0] == 'z'], reverse=True)
    binary = ''.join([str(j) for i, j in z_wires])
    print(f'Part 1 - Z values form the binary number {binary}, or decimal: {int(binary, 2)}')

def calculate(operats, results, order):
    for wire in order:
        a, b, op = operats[wire]
        results[wire] = op(results[a], results[b])

def kahn(S, is_deps, depends):
    L = []
    while S:
        n = S.pop()
        L.append(n)
        for m in is_deps[n]:
            depends[m].remove(n)
            if not depends[m]:
                S.add(m)
    # If there are still edges in depends[], graph is cyclic
    return L

def read_lines(filename):
    initial = re.compile(r'(\w+): (\d+)')
    boolean = re.compile(r'(\w+) (AND|OR|XOR) (\w+) -> (\w+)')
    depends = defaultdict(list)
    is_deps = defaultdict(list)
    results = {}
    operats = {}
    with open(filename) as lines:
        for line in lines:
            if initial.search(line):
                k, v = initial.search(line).groups()
                results[k] = int(v)
                operats[k] = (k, k, OPS['NUL'])
            if boolean.search(line):
                a, op, b, r = boolean.search(line).groups()
                depends[r].extend([a, b])
                is_deps[a].append(r)
                is_deps[b].append(r)
                operats[r] = (a, b, OPS[op])
    return depends, is_deps, operats, results

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
