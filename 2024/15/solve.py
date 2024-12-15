#!/usr/bin/env python
# encoding: utf-8

import argparse
import re

MOVEMENTS = {
    '^': ( 0, -1),
    '>': ( 1,  0),
    'v': ( 0,  1),
    '<': (-1,  0),
}
HORZ = ('<', '>')
VERT = ('^', 'v')

ENLARGE = {
    '#': '##',
    'O': '[]',
    '.': '..',
    '@': '@.',
}
BIGBOX = ('[', ']')


def main(args):
    maze, moves = read_lines(args.filename)
    walk_robot(maze, moves)
    boxes = find_element('O', maze)
    print(f'Part 1 - GPS coordinates sum is: {sum([x + 100*y for x, y in boxes])}')

    # maze, moves = read_lines(args.filename)
    # maze = enlarge(maze)
    # plot(maze)
    # walk_robot(maze, moves)
    # plot(maze)
    # boxes = find_element(r'\[\]', maze)
    # print(f'Part 2 - GPS coordinates sum is: {sum([x + 100*y for x, y in boxes])}')

def walk_robot(maze, moves):
    x, y = find_element('@', maze)[0]
    for move in moves:
        dx, dy = MOVEMENTS[move]
        if maze[y+dy][x+dx] == '.' or push_box(x+dx, y+dy, move, maze):
            # print(x, y, move)
            x, y = move_element(x, y, move, maze)
            # plot(maze)
            # print()

def push_box(x, y, move, maze):
    dx, dy = MOVEMENTS[move]

    # Normal Maze
    if maze[y][x] == 'O':
        if maze[y+dy][x+dx] == '.':
            move_element(x, y, move, maze)
            return True
        if maze[y+dy][x+dx] == 'O':
            if push_box(x+dx, y+dy, move, maze):
                move_element(x, y, move, maze)
                return True

    # Large Maze
    if maze[y][x] in BIGBOX:
        if move in HORZ:
            if maze[y][x+2*dx] == '.':
                move_element(x+dx, y, move, maze)
                move_element(x,    y, move, maze)
                return True
            if maze[y][x+2*dx] in BIGBOX:
                if push_box(x+2*dx, y, move, maze):
                    move_element(x+dx, y, move, maze)
                    move_element(x, y, move, maze)
                    return True
        if move in VERT:
            xx = x+1 if maze[y][x] == '[' else x-1
            if maze[y+dy][x] == maze[y+dy][xx] == '.':
                move_element(x, y, move, maze)
                move_element(xx, y, move, maze)
                return True
            if maze[y+dy][x] in BIGBOX or maze[y+dy][xx] in BIGBOX:
                if push_box(x+dx, y+dy, move, maze):
                    move_element(x, y, move, maze)
                    move_element(xx, y, move, maze)
                    return True

def find_element(symbol, maze):
    return [(m.start(), j) for j, line in enumerate(maze) for m in re.finditer(symbol, ''.join(line))]

def move_element(x, y, move, maze):
    dx, dy = MOVEMENTS[move]
    symbol = maze[y][x]
    maze[y][x] = '.'
    maze[y+dy][x+dx] = symbol
    return x+dx, y+dy

def enlarge(maze):
    return [[e for e in ''.join([ENLARGE[p] for p in line])] for line in maze]

def plot(maze):
    print(f'    {''.join([str(i // 10) if i >= 10 else ' ' for i in range(len(maze[0]))])}')
    print(f'    {''.join([str(i % 10) for i in range(len(maze[0]))])}')
    for i, line in enumerate(maze):
        print(f'{i:03} {''.join(line)}')

def read_lines(filename):
    with open(filename) as input:
        lines = input.readlines()
    maze = [[p for p in line.strip()] for line in lines if line.startswith('#')]
    moves = ''.join([line.strip() for line in lines if line[0] in ('^','>','v','<')])
    return maze, moves

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
