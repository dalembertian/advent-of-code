#!/usr/bin/env python
# encoding: utf-8

import argparse
import re

from collections import defaultdict

from dijkstra import *


def main(args):
    maze   = read_maze(args.filename)
    start  = find_element('S', maze)[0]
    finish = find_element('E', maze)[0]

    nodes = defaultdict(dict)
    find_path(start, start, '', maze, nodes)
    find_shortest_path(start, nodes)
    # print_nodes(nodes)

    path, cost = trace_back(start, finish, nodes)
    # plot(maze, invisible_walls=True, path=path)
    # print(f'Cost by Dijkstra: {cost}')
    # print(f'Nodes: {len(nodes)}')

    cheats = find_cheats(maze, start, path)
    # print(cheats)

    saves = []
    for cheat in cheats:
        p, c = try_cheat(maze, cheat, start, finish)
        saves.append(cost - c)
    # saves.sort()

    print(f'Part 1 - Cheats that save at least 100 picosseconds: {len([s for s in saves if s >= 100])}')

def try_cheat(maze, cheat, start, finish):
    maze = [maze[y][:] for y in range(len(maze))]
    x, y = cheat
    maze[y][x] = '.'

    nodes = defaultdict(dict)
    find_path(start, start, '', maze, nodes)
    find_shortest_path(start, nodes)
    path, cost = trace_back(start, finish, nodes)
    # plot(maze, invisible_walls=True, path=path)
    # print(f'Cost by Dijkstra: {cost}')
    # input()
    return path, cost

def find_cheats(maze, start, path):
    x, y = start
    cheats = []
    for move in path:
        for dx, dy in [(i, j) for m, (i, j) in MOVEMENTS.items() if m != move]:
            if maze[y+dy][x+dx] == '#' and maze[y+2*dy][x+2*dx] != '#':
                cheats.append((x+dx, y+dy))
        dx, dy = MOVEMENTS[move]
        x, y = x+dx, y+dy
    return set(cheats)

def find_path(this, prev, path, maze, nodes):
    x, y = this
    moves = moves_from_here(this, path, maze)

    # If this is a visited node (or END), just update the way here
    if maze[y][x] == 'E' or this in nodes.keys():
        add_node(this, prev, path, nodes)
        return

    # print_nodes(nodes)
    # plot(maze, start=(x, y), path=path)
    # print(f'FIND PATH - this: {this}, prev: {prev}, path: {path}, moves: {moves}')
    # input()

    # If it's a single path ahead, keep moving
    while len(moves) == 1:
        move = moves[0]
        path += move
        dx, dy = MOVEMENTS[move]
        x, y, m = x+dx, y+dy, move
        this = (x, y)
        if maze[y][x] == 'E':
            add_node(this, prev, path, nodes)
            return
        moves = moves_from_here(this, path, maze)

    # If it's a new node, assess each path coming out of it
    if len(moves) > 1:
        if this in nodes.keys():
            add_node(this, prev, path, nodes)
        else:
            # print(f'NEW NODE - this: {this}, prev: {prev}, path: {path}')
            add_node(this, prev, path, nodes)
            for move in moves:
                dx, dy = MOVEMENTS[move]
                nodes[this].setdefault('nodes', {})
                find_path((x+dx, y+dy), this, move, maze, nodes)

    # If there are no moves to be made, it's a dead end, ignore

def add_node(this, prev, path, nodes):
    if this == prev:
        return

    prev_nodes = nodes[prev].setdefault('nodes', {})
    this_nodes = nodes[this].setdefault('nodes', {})
    cost = len(path)

    # Only add a node if it's shorter then prev parallel one
    old_cost, old_path = this_nodes.get(prev, (INFINITE, ''))
    if cost < old_cost:
        nodes[prev]['nodes'][this] = (cost, path)
        nodes[this]['nodes'][prev] = (cost, invert_path(path))

def moves_from_here(this, path, maze):
    x, y = this
    came_from = OPPOSITE[path[-1]] if path else ''
    return [m for m, (dx, dy) in MOVEMENTS.items() if m != came_from and maze[y+dy][x+dx] != '#']

def find_element(symbol, maze):
    return [(m.start(), j) for j, line in enumerate(maze) for m in re.finditer(symbol, ''.join(line))]

def plot(maze, invisible_walls=False, start=None, path=None):
    maze = [maze[y][:] for y in range(len(maze))]
    if not start:
        start = find_element('S', maze)[0]
    if path:
        x, y = start
        for move in path:
            maze[y][x] = move
            dx, dy = MOVEMENTS[move]
            x, y = x+dx, y+dy

    plot_ruler(maze)
    for i, line in enumerate(maze):
        row = ''.join(line)
        if invisible_walls:
            row = row.replace('.', ' ')
            row = row.replace('#', '⋅')
        print(f'{i:03} {row} {i:03}')
    plot_ruler(maze)
    print()

def plot_ruler(maze):
    if len(maze[0]) >= 100:
        print(f'    {''.join([str(i // 100) if i >= 100 else ' ' for i in range(len(maze[0]))])}')
    print(f'    {''.join([str(i % 100 // 10) if i >= 10 else ' ' for i in range(len(maze[0]))])}')
    print(f'    {''.join([str(i % 10) for i in range(len(maze[0]))])}')

def read_maze(filename):
    with open(filename) as lines:
        maze = [['#'] + [p for p in line.strip()] + ['#'] for line in lines]
    maze.insert(0, ['#'] * len(maze[0]))
    maze.append(['#'] * len(maze[0]))
    return maze

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="Input file to process")
    args = parser.parse_args()
    main(args)
