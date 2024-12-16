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


def main(args):
    maze = read_lines(args.filename)

    nodes  = defaultdict(list)
    start  = find_element('S', maze)[0]
    finish = find_element('E', maze)[0]
    find_path(start, '>', start, '', maze, nodes)

    for k in nodes.keys():
        print(f'{k}: {nodes[k]}')
    # for end, path in nodes[start]:
    #     if end == finish:
    #         plot(maze, start, path)
    #         input()

def find_path(visit, move, previous, path, maze, nodes):
    x, y = visit
    path += move

    # for k in nodes.keys():
    #     print(f'{k}: {nodes[k]}')
    # plot(maze, visit, move)
    # print(f'From: {previous}')
    # input()

    if maze[y][x] in (' ', 'E'):
        nodes[previous].append((visit, path))
        nodes[visit].append((previous, invert_path(path)))
        return

    if maze[y][x] == 'S':
        path = ''

    maze[y][x] = ' '
    moves = [m for m, (dx, dy) in MOVEMENTS.items() if m != OPPOSITE[move] and maze[y+dy][x+dx] != '#']
    if len(moves) > 1:
        nodes[previous].append((visit, path))
        nodes[visit].append((previous, invert_path(path)))
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
        cost += 1 + 1000 if next_move != move else 0
        move = next_move
    return cost

def find_element(symbol, maze):
    return [(m.start(), j) for j, line in enumerate(maze) for m in re.finditer(symbol, ''.join(line))]

def plot(maze, start=None, path=None):
    maze = [maze[y][:] for y in range(len(maze))]
    if start and path:
        x, y = start
        for move in path:
            maze[y][x] = move
            dx, dy = MOVEMENTS[move]
            x, y = x+dx, y+dy
    print(f'    {''.join([str(i // 10) if i >= 10 else ' ' for i in range(len(maze[0]))])}')
    print(f'    {''.join([str(i % 10) for i in range(len(maze[0]))])}')
    for i, line in enumerate(maze):
        print(f'{i:03} {''.join(line)}')

def read_lines(filename):
    with open(filename) as lines:
        return [[p for p in line.strip()] for line in lines]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
