#!/usr/bin/env python
# encoding: utf-8

import argparse
import re

#from bisect import insort
# insort(list, element)
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


def main(args):
    maze = read_lines(args.filename)

    nodes  = defaultdict(dict)
    start  = find_element('S', maze)[0]
    finish = find_element('E', maze)[0]
    find_path(start, '>', start, '', maze, nodes)

    for k in nodes.keys():
        print(f'{k}: {nodes[k]}')

    # for node in nodes.keys():
    #     for end, path in nodes[node]['nodes']:
    #         if path:
    #             plot(maze, node, path)
    #             print(node, path)
    #             input()
    if dijkstra(start, finish, nodes, maze):
        node = finish
        path = ''
        while node != start:
            print(node, nodes[node]['prev_node'])
            path += nodes[node]['prev_path']
            node  = nodes[node]['prev_node']
        path = invert_path(path)
        plot(maze, start, path)
        print(f'Cost: {cost_path(path)}')

def dijkstra(start, finish, nodes, maze):
    # Mark all unvisited nodes with distance "infinite" from start - except start
    infinite = float('inf')
    unvisited = list(nodes.keys())
    for node in unvisited:        
        nodes[node]['cost'] = infinite
    nodes[start]['cost'] = 0

    while unvisited:
        # Get unvisited node with shortest distance to start
        unvisited.sort(key=lambda n: nodes[n]['cost'])
        plot(maze)
        print(unvisited)
        this = unvisited.pop(0)
        if nodes[this]['cost'] == infinite:
            break

        # Visits every node linked to this STILL IN unvisited
        print(this)
        for v, path in nodes[this]['nodes']:
            if v in unvisited:
                print(v, nodes[v].get('prev_node', None), nodes[v].get('cost', None), end='')
                cost = nodes[this]['cost'] + cost_path(path)
                if cost < nodes[v]['cost']:
                    nodes[v]['cost'] = cost
                    nodes[v]['prev_path'] = invert_path(path)
                    nodes[v]['prev_node'] = this
                    print(' -> ', nodes[v]['prev_node'], nodes[v]['cost'], end='')
                print()
        print()
        input()
    if not unvisited:
        return True

def find_path(visit, move, previous, path, maze, nodes):
    x, y = visit
    path += move

    # for k in nodes.keys():
    #     print(f'{k}: {nodes[k]}')
    # plot(maze, visit, move)
    # print(f'From: {previous}')
    # input()

    if maze[y][x] in (' ', 'E'):
        nodes[previous].setdefault('nodes', []).append((visit, path))
        nodes[visit].setdefault('nodes', []).append((previous, invert_path(path)))
        return

    if maze[y][x] == 'S':
        path = ''

    maze[y][x] = ' '
    moves = [m for m, (dx, dy) in MOVEMENTS.items() if m != OPPOSITE[move] and maze[y+dy][x+dx] != '#']
    if len(moves) > 1 and path:
        nodes[previous].setdefault('nodes', []).append((visit, path))
        nodes[visit].setdefault('nodes', []).append((previous, invert_path(path)))
        previous = visit
        path = ''

    for m in moves:
        dx, dy = MOVEMENTS[m]
        if m != OPPOSITE[move] and maze[y+dy][x+dx] != '#':
            find_path((x+dx, y+dy), m, previous, path, maze, nodes)

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
