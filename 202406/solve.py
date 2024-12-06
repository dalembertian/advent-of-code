#!/usr/bin/env python
# encoding: utf-8

import argparse

# x, y, next
MOVEMENTS = {
    '^': (-1,  0, '>'),
    '>': ( 0,  1, 'v'),
    'v': ( 1,  0, '<'),
    '<': ( 0, -1, '^'),
}

def main(args):
    maze = read_lines(args.filename)

    walk_guard(maze)
    print(f"Part 1 - Guard's route lenght is: {len(find_element('X', maze))}")

def read_lines(filename):
    maze = []
    with open(filename) as lines:
        for line in lines:
            maze.append(['O'] + [p for p in line.strip()] + ['O'])
    border = ['O' for i in range(len(maze[0]))]
    maze.insert(0, border)
    maze.append(border[:])
    return maze

def find_element(symbol, maze):
    found = []
    for i, row in enumerate(maze):
        for j, col in enumerate(row):
            if col == symbol:
                found.append((i,j))
    return found

def walk_guard(maze):
    pos = find_element('^', maze)[0]
    maxx, maxy = len(maze[0])-1, len(maze)-1
    while 0 < pos[0] < maxx and 0 < pos[1] < maxy:
        pos = step_guard(pos, maze)
    print_maze(maze)

def step_guard(pos, maze):
    # returns new pos, marking step done
    x, y = pos
    direction = maze[x][y]
    deltax, deltay, turn = MOVEMENTS[direction]
    while maze[x+deltax][y+deltay] == '#':
        direction = turn
        deltax, deltay, turn = MOVEMENTS[turn]
    maze[x][y] = 'X'
    maze[x+deltax][y+deltay] = direction
    return x+deltax, y+deltay

def print_maze(maze):
    for i, line in enumerate(maze):
        print(f'{i:03} {''.join(line)}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
