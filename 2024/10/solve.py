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
    plot(maze)

    trailheads = find_hikes(maze)
    print(f'Part 1 - Total sum of trailheads is: {sum(trailheads)}')

def find_hikes(maze):
    heads = []
    size = len(maze) - 2
    for row in range(size):
        for col in range(size):
            hike = check_trail(row, col, maze)
            if hike:
                heads.append(hike)
    return heads

def check_trail(row, col, maze, expected=0):
    x, y = row + 1, col + 1
    print(''.join([' ' for i in range(expected)]), row, col, maze[x][y], expected)
    if maze[x][y] != expected or maze[x][y] == -1:
        return 0
    elif maze[x][y] == expected:
        if expected == 9:
            return 1
        else:
            return check_trail(row - 1, col, maze, expected + 1) + \
                   check_trail(row + 1, col, maze, expected + 1) + \
                   check_trail(row, col - 1, maze, expected + 1) + \
                   check_trail(row, col + 1, maze, expected + 1)

def plot(maze):
    for row in maze:
        print(row)

def read_lines(filename):
    maze = []
    with open(filename) as lines:
        for line in lines:
            maze.append([-1] + [int(p) for p in line.strip()] + [-1])
    border = [-1 for i in range(len(maze[0]))]
    maze.insert(0, border)
    maze.append(border[:])
    return maze

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
