#!/usr/bin/env python
# encoding: utf-8

import argparse

from collections import deque, defaultdict

from dijkstra import *


def main(args):
    nodes = read_lines(args.filename)

    # Correct: 764
    # print(is_cyclic(nodes, 'you'))
    explore_nodes(nodes, 'you')
    print(f'Part 1 - exit paths from \'you\': {len(nodes['out'].get('previous', []))}')

    # Correct: 
    nodes['out'] = {}
    find_shortest_path(nodes, 'svr')
    print_nodes(nodes)
    print_paths(nodes, 'out')

    print(f'Part 2 - exit paths from \'svr\' passing by \'dac\' and \'fft\': {len(nodes['out'].get('previous', []))}')

def explore_nodes(nodes, start):
    # BFS traverse of nodes

    for node in nodes.keys():
        nodes[node].get('previous', []).clear()

    V = deque([start])
    while V:
        v = V.popleft()
        for node in nodes[v].get('next', []):
            nodes[node].setdefault('previous', []).append(v)
            V.append(node)


def is_cyclic(nodes, start):
    # DFS check looking for cycles
    visited = []
    current = []
    if is_current_cyclic(nodes, start, visited, current):
        return True
    return False


def is_current_cyclic(nodes, start, visited, current):
    # If already visited in this current check, it's cyclic
    if start in current:
        return True

    # If already visited previously, no need to check it again
    if start in visited:
        return False

    current.append(start)
    visited.append(start)
    links = nodes[start].get('next', [])
    if any([is_current_cyclic(nodes, link, visited, current) for link in links]):
        return True

    # Remove from current check before returning
    current.remove(start)
    return False


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
