#!/usr/bin/env python
# encoding: utf-8

import argparse

MOVEMENTS = {
    '^': (-1,  0),
    '>': ( 0,  1),
    'v': ( 1,  0),
    '<': ( 0, -1),
}


def main(args):
    maze, moves = read_lines(args.filename)
    plot(maze)
    print(moves)

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
