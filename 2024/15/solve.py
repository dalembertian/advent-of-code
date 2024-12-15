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


def main(args):
    maze, moves = read_lines(args.filename)

    walk_robot(maze, moves)
    plot(maze)
    boxes = find_element('O', maze)
    print(f'Part 1 - GPS coordinates sum is: {sum([x + 100*y for x, y in boxes])}')

def walk_robot(maze, moves):
    x, y = find_element('@', maze)[0]
    for move in moves:
        dx, dy = MOVEMENTS[move]
        # print(f'({x},{y}) -> ({x+dx},{x+dy})')
        if maze[y+dy][x+dx] == '.' or push_box(x+dx, y+dy, move, maze):
            x, y = move_element('@', x, y, move, maze)

def push_box(x, y, move, maze):
    if maze[y][x] == 'O':
        dx, dy = MOVEMENTS[move]
        if maze[y+dy][x+dx] == '.':
            move_element('O', x, y, move, maze)
            return True
        elif maze[y+dy][x+dx] == 'O':
            if push_box(x+dx, y+dy, move, maze):
                move_element('O', x, y, move, maze)
                return True
        else:
            return False

def find_element(symbol, maze):
    return [(m.start(), j) for j, line in enumerate(maze) for m in re.finditer(symbol, ''.join(line))]

def move_element(symbol, x, y, move, maze):
    dx, dy = MOVEMENTS[move]
    maze[y][x] = '.'
    maze[y+dy][x+dx] = symbol
    return x+dx, y+dy

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
