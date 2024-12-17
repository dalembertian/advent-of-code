#!/usr/bin/env python
# encoding: utf-8

import argparse
import re

from collections import defaultdict

MOVEMENTS = {
    '^': ( 0, -1),
    '>': ( 1,  0),
    'v': ( 0,  1),
    '<': (-1,  0),
}
OPPOSITE = {
    '^': 'v',
    '>': '<',
    'v': '^',
    '<': '>',
}
INFINITE = float('inf')


def main(args):
    maze = read_lines(args.filename)
    plot(maze)

    nodes  = defaultdict(dict)
    start  = find_element('S', maze)[0]
    finish = find_element('E', maze)[0]
    find_path(start, '>', start, 0, '', maze, nodes)
    # Two problems with the nodes collected:
    # 1. The distances are wrong, because the path to get to a certain node will
    #    influence the NEXT paths going out (because of the orientation of the reindeer).
    #    Fixing this will be a PITA.
    # 2. The recursive approach to give each and every step was a mistake: the stack is
    #    overflowing even for Part 1. A possible fix would be to follow unique paths
    #    iteratively, and throw new paths to follow (after a node) to a list.

    for k in nodes.keys():
        print(f'{k}: {nodes[k]}')
    print()

    path, cost = dijkstra(start, nodes, maze)
    if path:
        plot(maze, start, path)
        print(f'Cost by Dijkstra: {cost}')

def find_path(visit, move, previous, initial_cost, path, maze, nodes):
    x, y = visit
    path += move

    # for k in nodes.keys():
    #     print(f'{k}: {nodes[k]}')
    # plot(maze, visit, move)
    # print(f'From: {previous}')
    # input()

    if maze[y][x] in (' ', 'E'):
        add_node(visit, previous, initial_cost, path, nodes)
        return

    if maze[y][x] == 'S':
        path = ''

    maze[y][x] = ' '
    moves = [m for m, (dx, dy) in MOVEMENTS.items() if m != OPPOSITE[move] and maze[y+dy][x+dx] != '#']
    if len(moves) > 1 and path:
        add_node(visit, previous, initial_cost, path, nodes)
        previous = visit
        path = ''

    for m in moves:
        dx, dy = MOVEMENTS[m]
        if m != OPPOSITE[move] and maze[y+dy][x+dx] != '#':
            cost = initial_cost if path != '' else (0 if m == move else 1000)
            find_path((x+dx, y+dy), m, previous, cost, path, maze, nodes)

def add_node(this, previous, initial_cost, path, nodes):
    new_cost = initial_cost + cost_path(path)
    prev_nodes = nodes[previous].setdefault('nodes', {})
    this_nodes = nodes[this].setdefault('nodes', {})
    # Only add a node if it's shorter then previous parallel one
    old_cost, old_path = this_nodes.get(previous, (INFINITE, ''))
    if new_cost < old_cost:
        nodes[previous]['nodes'][this] = (new_cost, path)
        nodes[this]['nodes'][previous] = (new_cost, invert_path(path))

def invert_path(path):
    return ''.join([OPPOSITE[move] for move in path[::-1]])

def cost_path(path):
    cost = 0
    move = path[0]
    for next_move in path:
        cost += 1 if next_move == move else 1001
        move = next_move
    return cost

def find_element(symbol, maze):
    return [(m.start(), j) for j, line in enumerate(maze) for m in re.finditer(symbol, ''.join(line))]

def dijkstra(start, nodes, maze):
    # Mark all unvisited nodes with distance "infinite" from start - except start
    unvisited = list(nodes.keys())
    for node in unvisited:
        nodes[node]['cost'] = INFINITE
    nodes[start]['cost'] = 0

    while unvisited:
        # Get unvisited node with shortest distance to start
        unvisited.sort(key=lambda n: nodes[n]['cost'])
        # plot(maze)
        # print(unvisited)
        this = unvisited.pop(0)
        if nodes[this]['cost'] == INFINITE:
            break

        # Visits every node linked to this STILL IN unvisited
        # print(this)
        for v, (cost, path) in nodes[this]['nodes'].items():
            if v in unvisited:
                # print(v, nodes[v].get('prev_node', None), nodes[v].get('cost', None), end='')
                new_cost = nodes[this]['cost'] + cost
                if new_cost < nodes[v]['cost']:
                    nodes[v]['cost'] = new_cost
                    nodes[v]['prev_path'] = invert_path(path)
                    nodes[v]['prev_node'] = this
        #             print(' -> ', nodes[v]['prev_node'], nodes[v]['cost'], end='')
        #         print()
        # print()
        # input()
    if unvisited:
        return '', 0

    # Builds path from finish to start
    finish = find_element('E', maze)[0]
    node = finish
    path = ''
    while node != start:
        print(f'{str(node):8} -> {str(nodes[node]['prev_node']):8}: {nodes[node]['cost']:5} {nodes[node]['prev_path']}')
        path += nodes[node]['prev_path']
        node  = nodes[node]['prev_node']
    return invert_path(path), nodes[finish]['cost']

def plot(maze, start=None, path=None):
    cost = 0
    maze = [maze[y][:] for y in range(len(maze))]
    if start and path:
        x, y = start
        previous = path[0]
        for move in path:
            cost += 1 if move == previous else 1001
            previous = move
            maze[y][x] = move
            dx, dy = MOVEMENTS[move]
            x, y = x+dx, y+dy
    print(f'    {''.join([str(i // 10) if i >= 10 else ' ' for i in range(len(maze[0]))])}')
    print(f'    {''.join([str(i % 10) for i in range(len(maze[0]))])}')
    for i, line in enumerate(maze):
        print(f'{i:03} {''.join(line)}')
    print(f'Cost: {cost}')

def read_lines(filename):
    with open(filename) as lines:
        return [[p for p in line.strip()] for line in lines]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
