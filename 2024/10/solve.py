#!/usr/bin/env python
# encoding: utf-8

import argparse

def main(args):
    maze = read_lines(args.filename)
    plot(maze)

    trailheads = find_hikes(maze)
    print(f'Part 1 - Total sum of trailheads is: {sum(trailheads)}')

    trailheads = find_hikes(maze, unique=False)
    print(f'Part 2 - Total sum of SCORE of trailheads is: {sum(trailheads)}')

def find_hikes(maze, unique=True):
    heads = []
    size = len(maze) - 2
    for row in range(size):
        for col in range(size):
                trails = check_trail(row, col, maze)
                if unique:
                    trails = set(trails)
                heads.append(len(trails))
    return heads

def check_trail(row, col, maze, expected=0):
    x, y = row + 1, col + 1
    # print(''.join([' ' for i in range(expected)]), x, y, maze[x][y], expected)
    if maze[x][y] != expected or maze[x][y] == '.':
        return []
    elif maze[x][y] == expected:
        if expected == 9:
            return [(row,col)]
        else:
            return check_trail(row - 1, col, maze, expected + 1) + \
                   check_trail(row + 1, col, maze, expected + 1) + \
                   check_trail(row, col - 1, maze, expected + 1) + \
                   check_trail(row, col + 1, maze, expected + 1)

def plot(maze):
    for row in maze:
        print(''.join([str(c) for c in row]))

def read_lines(filename):
    maze = []
    with open(filename) as lines:
        for line in lines:
            maze.append(['.'] + [int(p) for p in line.strip()] + ['.'])
    border = ['.' for i in range(len(maze[0]))]
    maze.insert(0, border)
    maze.append(border[:])
    return maze

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
