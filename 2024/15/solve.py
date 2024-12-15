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

    maze, moves = read_lines(args.filename)
    maze = enlarge(maze)
    walk_robot(maze, moves)
    boxes = find_element(r'\[', maze)
    print(f'Part 2 - GPS coordinates sum is: {sum([x + 100*y for x, y in boxes])}')

def walk_robot(maze, moves):
    x, y = find_element('@', maze)[0]
    for i, move in enumerate(moves):
        dx, dy = MOVEMENTS[move]
        if maze[y+dy][x+dx] == '.' or push_boxes([(x+dx, y+dy)], move, maze):
            x, y = move_element(x, y, move, maze)

def push_boxes(boxes, move, maze):
    dx, dy = MOVEMENTS[move]
    x, y = boxes[0]

    # Normal Maze
    if maze[y][x] == 'O':
        if maze[y+dy][x+dx] == '.':
            move_element(x, y, move, maze)
            return True
        if maze[y+dy][x+dx] == 'O':
            if push_boxes([(x+dx, y+dy)], move, maze):
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
                if push_boxes([(x+2*dx, y)], move, maze):
                    move_element(x+dx, y, move, maze)
                    move_element(x, y, move, maze)
                    return True
        if move in VERT:
            # Both [ and ] should be in the list of boxes
            for i, j in boxes:
                ii = i+1 if maze[j][i] == '[' else i-1
                if (ii, j) not in boxes:
                    boxes.append((ii,j))
            if all([maze[j+dy][i+dx] == '.' for i, j in boxes]):
                for i, j in boxes:
                    move_element(i, j, move, maze)
                return True
            if any([maze[j+dy][i+dx] == '#' for i, j in boxes]):
                return False
            if any([maze[j+dy][i+dx] in BIGBOX for i, j in boxes]):
                if push_boxes([(i+dx, j+dy) for i, j in boxes if maze[j+dy][i+dx] in BIGBOX], move, maze):
                    for i, j in boxes:
                        move_element(i, j, move, maze)
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
