#!/usr/bin/env python
# encoding: utf-8

import argparse
import re

from collections import defaultdict
from itertools import permutations


def main(args):
    pairs = read_lines(args.filename)

    net = defaultdict(set)
    for i, j in pairs:
        net[i].add(j)
        net[j].add(i)
    # for k, v in net.items():
    #     print(k, v)

    triples = set()
    for a in net.keys():
        for b in net[a]:
            inter = net[a].intersection(net[b])
            while inter:
                triple = (a, b, inter.pop())
                if not triples.intersection(permutations(triple)):
                    triples.add(triple)

    total = 0
    for triple in triples:
        total += 1 if any([1 if c[0] == 't' else 0 for c in triple]) else 0
    print(f'Part 1 - Possible triples with Santa in: {total}')

def read_lines(filename):
    with open(filename) as input:
        return [tuple(line.strip().split('-')) for line in input.readlines()]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
