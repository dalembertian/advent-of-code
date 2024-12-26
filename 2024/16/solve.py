#!/usr/bin/env python
# encoding: utf-8

import argparse
import re
import sys

from collections import defaultdict

from dijkstra import *


def main(args):
    sys.setrecursionlimit(2000)

    maze = read_lines(args.filename)
    S = find_element('S', maze)[0]
    E = find_element('E', maze)[0]
    # plot(maze)
    # print()

    x, y = S
    start = (x, y, '>')
    nodes = defaultdict(dict)
    find_path(start, start, '', maze, nodes)
    find_shortest_path(start, nodes)
    # print_nodes(nodes)

    finish = find_best_finish(start, E, nodes)
    path, cost = trace_back(start, finish, nodes)
    # plot(maze, invisible_walls=True, path=path)
    # print(f'Cost by Dijkstra: {cost}')
    # print(f'Nodes: {len(nodes)}')
    print(f'Part 1 - Cost of the shortest path: {cost}')

    steps = find_all_steps(start, finish, nodes)
    # plot(maze, invisible_walls=True, steps=steps)
    print(f'Part 2 - Tiles that are part of ANY of the shortest paths: {len(steps)}')

def find_best_finish(start, E, nodes):
    best_cost = INFINITE
    best_finish = None
    fx, fy = E
    for movement in MOVEMENTS.keys():
        finish = (fx, fy, movement)
        path, cost = trace_back(start, finish, nodes)
        # print(f'Finish: {finish}, cost: {cost}')
        if cost < best_cost:
            best_cost = cost
            best_finish = finish
    return best_finish

def find_all_steps(start, finish, nodes):
    if finish == start:
        x, y, m = start
        return [(x, y)]
    else:
        steps = set()
        for node, path in zip(nodes[finish]['prev_node'], nodes[finish]['prev_path']):
            x, y, m = finish
            for move in path:
                steps.add((x, y))
                dx, dy = MOVEMENTS[move]
                x, y = x+dx, y+dy
            steps.update(find_all_steps(start, node, nodes))
    return steps

def find_path(this, prev, path, maze, nodes):
    x, y, m = this

    moves = moves_from_here(this, maze)
    
    # If it's a single path ahead, keep moving
    while len(moves) == 1:
        move = moves[0]
        path += move
        dx, dy = MOVEMENTS[move]
        x, y, m = x+dx, y+dy, move
        this = (x, y, m)

        # Might encounter START or END in a single path
        if maze[y][x] in ('S', 'E'): 
            add_node(this, prev, path, nodes)
            find_path(this, this, '', maze, nodes)
            return

        moves = moves_from_here(this, maze)

    # If it's a node...
    if len(moves) > 1:
        if this in nodes.keys():
            # ... already visited, just finish the path to it
            add_node(this, prev, path, nodes)
        else:
            # ... never seen before, mark it and try every path out of it
            for move in moves:
                dx, dy = MOVEMENTS[move]
                add_node(this, prev, path, nodes)
                find_path((x+dx, y+dy, move), (x, y, m), move, maze, nodes)

    # If there are no moves to be made, it's a dead end, ignore
    # if len(moves) < 0...

def add_node(this, prev, path, nodes):
    prev_nodes = nodes[prev].setdefault('nodes', {})
    this_nodes = nodes[this].setdefault('nodes', {})
    cost = 0 if not path else (cost_path(path) + (0 if prev[2] == path[0] else 1000))

    # Only add a node if it's shorter then prev parallel one
    old_cost, old_path = this_nodes.get(prev, (INFINITE, ''))
    if cost < old_cost:
        nodes[prev]['nodes'][this] = (cost, path)
        nodes[this]['nodes'][prev] = (cost, invert_path(path))

def moves_from_here(this, maze):
    x, y, move = this
    return [m for m, (dx, dy) in MOVEMENTS.items() if m != OPPOSITE[move] and maze[y+dy][x+dx] != '#']

def cost_path(path):
    cost = 0
    move = path[0]
    for next_move in path:
        cost += 1 if next_move == move else 1001
        move = next_move
    return cost

def find_element(symbol, maze):
    return [(m.start(), j) for j, line in enumerate(maze) for m in re.finditer(symbol, ''.join(line))]

def plot(maze, invisible_walls=False, start=None, path=None, steps=None):
    # print(f'PLOT - start: {start}, path: {path}')
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

    if steps:
        for x, y in steps:
            maze[y][x] = 'O'

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

def read_lines(filename):
    with open(filename) as lines:
        return [[p for p in line.strip()] for line in lines]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
