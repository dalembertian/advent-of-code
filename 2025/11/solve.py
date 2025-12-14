#!/usr/bin/env python
# encoding: utf-8

import argparse

from collections import defaultdict

from graph import *


def main(args):
    nodes = read_lines(args.filename)

    # Correct: 764
    # print(is_cyclic(nodes, 'you'))
    map_previous_nodes(nodes, 'you')
    print(f'Part 1 - exit paths from \'you\': {len(nodes['out'].get('previous', []))}')

    # find_shortest_path(nodes, 'svr', True)
    # print(f'{nodes['out'].get('count', 0)}')
    # print_paths(nodes, 'out')
    # print()

    # Incorrect: 4563341276580 (too low)
    print(f'Part 2 - exit paths from \'svr\' passing by \'dac\' and \'fft\': {count_paths(nodes, ['dac', 'fft'])}')

    # Correct: 462444153119850


def count_paths(nodes, passing_by):
    first, second = passing_by
    runs = [['svr', first, second, 'out'], ['svr', second, first, 'out']]
    total = 0
    for run in runs:
        subtotal = 1
        for i in range(3):
            find_shortest_path(nodes, run[i])
            subtotal *= nodes[run[i+1]].get('count', 0)
        total += subtotal
    return total


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
