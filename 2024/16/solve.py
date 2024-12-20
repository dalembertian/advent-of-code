#!/usr/bin/env python
# encoding: utf-8

import argparse
import re
import sys

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
    sys.setrecursionlimit(2000)

    maze = read_lines(args.filename)
    # plot(maze)
    # print()

    nodes  = defaultdict(dict)
    start  = find_element('S', maze)[0]
    finish = find_element('E', maze)[0]

    x, y = start
    this = (x, y, '>')
    find_path(this, this, '', maze, nodes)
    # for k in nodes.keys():
    #     print(f'{k}: {nodes[k]}')
    # print()

    path, cost = dijkstra(start, finish, nodes, maze)
    # if path:
    #     plot(maze, start, path)
    #     print(f'Cost by Dijkstra: {cost}')
    # print(f'Nodes: {len(nodes)}')

    print(f'Part 1 - Cost of the shortest path: {cost}')

def find_path(this, prev, path, maze, nodes):
    x, y, m = this

    # for k in nodes.keys():
    #     print(f'{k}: {nodes[k]}')
    # plot(maze, (x, y), path)
    # print(f'FIND PATH - this: {this}, prev: {prev}, path: {path}')
    # input()

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

    # If it's a new node, assess each path coming out of it
    if len(moves) > 1:
        if this in nodes.keys():
            # print(f'VISITED NODE - this: {this}, prev: {prev}, path: {path}')
            add_node(this, prev, path, nodes)
        else:
            # print(f'NEW NODE - this: {this}, prev: {prev}, path: {path}')
            for move in moves:
                dx, dy = MOVEMENTS[move]
                add_node(this, prev, path, nodes)
                find_path((x+dx, y+dy, move), (x, y, m), move, maze, nodes)

    # If there are no moves to be made, it's a dead end, ignore

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

def dijkstra(start, finish, nodes, maze):
    sx, sy = start
    start = (sx, sy, '>')

    # Mark all unvisited nodes with distance "infinite" from start - except start
    unvisited = list(nodes.keys())
    for node in unvisited:
        nodes[node]['cost'] = INFINITE
    nodes[start]['cost'] = 0

    while unvisited:
        # Get unvisited node with shortest distance to start
        unvisited.sort(key=lambda n: nodes[n]['cost'])
        this = unvisited.pop(0)
        if nodes[this]['cost'] == INFINITE:
            break

        # Visits every node linked to this STILL IN unvisited
        for v, (cost, path) in nodes[this]['nodes'].items():
            if v in unvisited:
                new_cost = nodes[this]['cost'] + cost
                if new_cost < nodes[v]['cost']:
                    nodes[v]['cost'] = new_cost
                    nodes[v]['prev_path'] = invert_path(path)
                    nodes[v]['prev_node'] = this
    if unvisited:
        return '', 0

    # Builds path from finish to start for the 4 possible end nodes
    fx, fy = finish
    best_path = ''
    best_cost = INFINITE
    for movement in MOVEMENTS.keys():
        finish = (fx, fy, movement)
        node = finish
        if nodes[node]:
            path = ''
            while node != start:
                path += nodes[node]['prev_path']
                node  = nodes[node]['prev_node']
            if nodes[finish]['cost'] < best_cost:
                best_cost = nodes[finish]['cost']
                best_path = path
    return invert_path(best_path), best_cost

def plot(maze, start=None, path=None):
    # print(f'PLOT - start: {start}, path: {path}')
    cost = 0
    maze = [maze[y][:] for y in range(len(maze))]
    if not start:
        start = find_element('S', maze)[0]
    if path:
        x, y = start
        prev = path[0]
        for move in path:
            cost += 1 if move == prev else 1001
            prev = move
            maze[y][x] = move
            dx, dy = MOVEMENTS[move]
            x, y = x+dx, y+dy
    if len(maze[0]) >= 100:
        print(f'    {''.join([str(i // 100) if i >= 100 else ' ' for i in range(len(maze[0]))])}')
    print(f'    {''.join([str(i % 100 // 10) if i >= 10 else ' ' for i in range(len(maze[0]))])}')
    print(f'    {''.join([str(i % 10) for i in range(len(maze[0]))])}')
    for i, line in enumerate(maze):
        print(f'{i:03} {''.join(line)} {i:03}')
    print(f'    {''.join([str(i % 10) for i in range(len(maze[0]))])}')
    print(f'    {''.join([str(i % 100 // 10) if i >= 10 else ' ' for i in range(len(maze[0]))])}')
    if len(maze[0]) >= 100:
        print(f'    {''.join([str(i // 100) if i >= 100 else ' ' for i in range(len(maze[0]))])}')
    # print(f'Cost: {cost}')

def read_lines(filename):
    with open(filename) as lines:
        return [[p for p in line.strip()] for line in lines]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
