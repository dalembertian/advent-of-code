#!/usr/bin/env python
# encoding: utf-8

from argparse import ArgumentParser
from collections import defaultdict
from functools import reduce
from re import compile

        
def main(args):
    width, length, positions, velocities = read_lines(args.filename)
    plot(width, length, positions)
    print()

    move_robots(width, length, positions, velocities, 100)
    plot(width, length, positions)
    print()

    quadrants = safe(width, length, positions)
    print(quadrants)
    print(reduce(lambda x, y: x * y, quadrants))

def plot(width, length, positions):
    maze = [[0 for j in range(width)] for i in range(length)]
    for x, y in positions:
        maze[y][x] += 1
    for row in maze:
        print(''.join([str(p) for p in row]))
    return maze

def plot(width, length, positions):
    maze = [[0 for j in range(width)] for i in range(length)]
    for x, y in positions:
        maze[y][x] += 1
    for row in maze:
        print(''.join([str(p) if p>0 else '.' for p in row]))

def move_robots(width, length, positions, velocities, times):
    for i, (x, y) in enumerate(positions):
        positions[i] = (
            (x + times * velocities[i][0]) % width,
            (y + times * velocities[i][1]) % length,
        )

def safe(width, length, positions):
    mx, my = width // 2, length // 2
    robots = defaultdict(int)
    for x, y in positions:
        if x != mx and y != my:
            robots[(0 if x < mx else 1, 0 if y < my else 1)] += 1
    print(robots)
    return robots.values()

def read_lines(filename):
    values = compile(r'(-?\d+)')
    positions, velocities = [], []
    with open(filename) as input:
        width, length = map(int, values.findall(input.readline()))
        lines = input.readlines()
        for line in lines:
            px, py, vx, vy = map(int, values.findall(line))
            positions.append((px, py))
            velocities.append((vx, vy))
    return width, length, positions, velocities

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
