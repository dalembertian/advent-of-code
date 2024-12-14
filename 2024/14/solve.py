#!/usr/bin/env python
# encoding: utf-8

from argparse import ArgumentParser
from collections import defaultdict
from functools import reduce
from re import compile

        
def main(args):
    width, length, positions, velocities = read_lines(args.filename)
    move_robots(width, length, positions, velocities, 100)
    quadrants = safe(width, length, positions)
    print(f'Part 1 - Safety factor is: {reduce(lambda x, y: x * y, quadrants)}')

    width, length, positions, velocities = read_lines(args.filename)
    easter_eggs = find_easter_egg(width, length, positions, velocities)
    for egg in easter_eggs:
        print(f'Part 2 - Possible Easter Egg after {egg} seconds:')
        egg_positions = positions[:]
        move_robots(width, length, egg_positions, velocities, egg)
        plot(width, length, egg_positions)

def find_easter_egg(width, length, positions, velocities):
    # "(...) very rarely, most of the robots should arrange themselves into a picture
    # of a Christmas tree".
    # Very little detail given, I assume it means non-overlapping robots
    # TODO: Change to look for the "frame"!
    solutions = []
    for i in range(10000):
        robots = defaultdict(int)
        success = True
        for (x, y), (vx, vy) in zip(positions, velocities):
            nx = (x + i * vx) % width
            ny = (y + i * vy) % length
            if robots[(nx, ny)] != 0:
                success = False
                break
            else:
                robots[(nx, ny)] = 1
        if success:
            solutions.append(i)
    return solutions

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
    return robots.values()

def plot(width, length, positions):
    maze = [[0 for j in range(width)] for i in range(length)]
    for x, y in positions:
        maze[y][x] += 1
    for row in maze:
        print(''.join([str(p) if p>0 else '.' for p in row]))
    print()

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
