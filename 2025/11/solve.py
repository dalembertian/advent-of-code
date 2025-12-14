#!/usr/bin/env python
# encoding: utf-8

import argparse
from collections import defaultdict
from functools import cache

from graph import *


nodes = defaultdict(dict)


def main(args):
    nodes.update(read_lines(args.filename))

    # Correct: 764
    # print(is_cyclic(nodes, 'you'))
    map_previous_nodes(nodes, 'you')
    print(f'Part 1 - exit paths from \'you\': {len(nodes['out'].get('previous', []))}')

    # find_shortest_path(nodes, 'svr', True)
    # print(f'{nodes['out'].get('count', 0)}')
    # print_paths(nodes, 'out')
    # print()

    # Incorrect: 4563341276580 (too low)
    # After struggling with this modified Dijkstra, I can't find what's wrong. Movingn on to a cached solution...
    print(f'Part 2 - exit paths from \'svr\' passing by \'dac\' and \'fft\': {count_paths(nodes, ['dac', 'fft'])}')

    # Correct: 462444153119850
    paths = (traverse_next_nodes('svr', 'dac') * traverse_next_nodes('dac', 'fft') * traverse_next_nodes('fft', 'out')
           + traverse_next_nodes('svr', 'fft') * traverse_next_nodes('fft', 'dac') * traverse_next_nodes('dac', 'out'))
    print(f'Part 2 - exit paths from \'svr\' passing by \'dac\' and \'fft\': {paths}')


@cache
def traverse_next_nodes(start, finish):
    if start == finish:
        return 1
    return sum([traverse_next_nodes(node, finish) for node in nodes[start].get('next', [])])


def map_previous_nodes(nodes, start):
    # BFS traverse of nodes

    for node in nodes.keys():
        nodes[node].get('previous', []).clear()

    V = deque([start])
    while V:
        v = V.popleft()
        for node in nodes[v].get('next', []):
            nodes[node].setdefault('previous', []).append(v)
            V.append(node)


def read_lines(filename):
    nodes = defaultdict(dict)
    with open(filename) as lines:
        for line in lines:
            nodes[line[:3]]['next'] = line[5:].split()
    return nodes


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
