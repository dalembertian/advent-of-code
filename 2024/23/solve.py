#!/usr/bin/env python
# encoding: utf-8

import argparse
import re

from collections import defaultdict
from itertools import permutations


def main(args):
    pairs = read_lines(args.filename)

    net = find_network(pairs)
    print(f'Part 1 - possible triples with Santa in: {find_triples(net)}')

    largest = find_largest(net)
    print(f'Part 2 - largest network: {largest}')

def find_largest(net):
    cliques = []
    bron_kerbosch(set(), set(net.keys()), set(), cliques, net)
    cliques.sort(key=lambda n: len(n))
    return ','.join(sorted(list(cliques[-1])))

def bron_kerbosch(R, P, X, cliques, net):
    if not len(P) and not len(X):
        cliques.append(R)
    for v in P:
        bron_kerbosch(R | {v}, P & net[v], X & net[v], cliques, net)
        P = P - {v}
        X = X | {v}

def find_triples(net):
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
    return total

def find_network(pairs):
    net = defaultdict(set)
    for i, j in pairs:
        net[i].add(j)
        net[j].add(i)
    # for k, v in net.items():
    #     print(k, v)
    return net

def read_lines(filename):
    with open(filename) as input:
        return [tuple(line.strip().split('-')) for line in input.readlines()]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
