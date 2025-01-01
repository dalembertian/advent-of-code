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
    maze   = read_maze(args.filename)
    start  = find_element('S', maze)[0]
    finish = find_element('E', maze)[0]

    path, visited = find_path(start, finish, maze)
    # plot(maze, invisible_walls=True, path=path)
    # print(f'Start: {start}, Finish: {finish}, Length: {len(path)}, {len(visited)}\n')

    cheats = find_cheats(start, 2, visited, maze)
    saves = sorted(cheats.values())
    print(f'Part 1 - Cheats that save at least 100 picosseconds: {len([s for s in saves if s >= 100])}')

    cheats = find_cheats(start, 20, visited, maze)
    saves = sorted(cheats.values())
    print(f'Part 2 - Cheats that save at least 100 picosseconds: {len([s for s in saves if s >= 100])}')
    # groups = defaultdict(int)
    # for s in saves: groups[s] += 1
    # for g in groups.keys(): print(f'{groups[g]} cheats saving {g} picosseconds')

def find_cheats(start, radius, visited, maze):
    cheats = {}
    size = len(maze[0]) - 1
    for this, i in visited.items():
        for dx in range(-radius, radius+1):
            for dy in range(-radius, radius+1):
                x, y = this
                taxi = abs(dx)+abs(dy)
                if taxi <= radius and x+dx > 0 and x+dx < size and y+dy > 0 and y+dy < size:
                    cheat = (x+dx, y+dy)
                    visit = visited.get(cheat, 0)
                    if visit > taxi + i:
                        cheats[(this,cheat)] = visit - i - taxi
    return cheats

def find_path(start, finish, maze):
    visited = {start: 0}
    i = 0
    path = ''
    this = start
    moves = moves_from_here(this, path, maze)
    while this != finish:
        i += 1
        move = moves[0]
        path += move
        (x, y), (dx, dy) = this, MOVEMENTS[move]
        this = (x+dx, y+dy)
        visited[this] = i
        moves = moves_from_here(this, path, maze)
    return path, visited

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
        return [[p for p in line.strip()] for line in lines]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="Input file to process")
    args = parser.parse_args()
    main(args)
