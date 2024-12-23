#!/usr/bin/env python
# encoding: utf-8

import argparse
import re
import sys

from collections import defaultdict

from dijkstra import *


def main(args):
    sys.setrecursionlimit(4000)

    size  = int(args.size) if args.size else 71
    first = int(args.first) if args.first else 1024
    walls = read_coordinates(args.filename)
    maze  = create_maze(size)
    insert_walls(walls[:first], maze)

    nodes  = defaultdict(dict)
    start  = find_element('S', maze)[0]
    finish = find_element('E', maze)[0]

    find_path(start, start, '>', maze, nodes)
    find_shortest_path(start, nodes)
    # print_nodes(nodes)
    # plot(maze)

    # Part 1
    # ./solve.py -s 7 -f 12 1_test.txt => 24 moves
    # ./solve.py -f 1024 input.txt => 302 moves
    path, cost = trace_back(start, finish, nodes)
    print(f'Part 1 - Cost of the shortest path: {cost}')
    # plot(maze, invisible_walls=True, path=path)
    # print(f'Cost by Dijkstra: {cost}')
    # print(f'Nodes: {len(nodes)}')

    # Part 2
    # TODO: implement a binary search!
    for i in range(len(walls) - first):
        insert_walls(walls[first+i: first+i+1], maze)
        find_path(start, start, '>', maze, nodes)
        find_shortest_path(start, nodes)
        path, cost = trace_back(start, finish, nodes)
        if not path:
            break
    print(f'Part 2 - No exit after {first+i} bytes fall, at {walls[first]}')

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
    move = path[-1]
    return [m for m, (dx, dy) in MOVEMENTS.items() if m != OPPOSITE[move] and maze[y+dy][x+dx] != '#']

def find_element(symbol, maze):
    return [(m.start(), j) for j, line in enumerate(maze) for m in re.finditer(symbol, ''.join(line))]

def plot(maze, invisible_walls=False, start=None, path=None):
    maze = [maze[y][:] for y in range(len(maze))]
    if not start:
        start = find_element('S', maze)[0]
    if path:
        x, y = start
        prev = path[0]
        for move in path:
            prev = move
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

def insert_walls(walls, maze):
    for x, y in walls:
        maze[y+1][x+1] = '#'

def create_maze(size):
    row = [c for c in ('#' + '.' * size + '#')]
    border = [c for c in '#' * (size +2)]
    maze = [row[:] for i in range(size)]
    maze.insert(0, border[:])
    maze.append(border[:])
    maze[1][1] = 'S'
    maze[-2][-2] = 'E'
    return maze

def read_coordinates(filename):
    values = re.compile(r'(\d+),(\d+)')
    with open(filename) as input:
        return [(int(x), int(y)) for x, y in [values.search(line).groups() for line in input.readlines()]]

def read_maze(filename):
    with open(filename) as lines:
        return [[p for p in line.strip()] for line in lines]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="Input file to process")
    parser.add_argument("-s", "--size", help="Size of the maze (default: 71)")
    parser.add_argument("-f", "--first", help="First walls to apply (default: 1024)")
    args = parser.parse_args()
    main(args)
