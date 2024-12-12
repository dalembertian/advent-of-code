#!/usr/bin/env python
# encoding: utf-8

import argparse
from collections import defaultdict
        
DIRECTIONS = ((-1, 0), (1, 0), (0, -1), (0, 1))

def main(args):
    maze = read_lines(args.filename)
    prices = find_regions(maze)
    print(f'Part 1 - Total price paid is: {sum(prices)}')

    maze = read_lines(args.filename)
    prices = find_regions(maze, discount=True)
    print(f'Part 2 - Total price paid is: {sum(prices)}')

def find_regions(maze, discount=False):
    prices = []
    size = len(maze) - 2
    for row in range(size):
        for col in range(size):
            region = maze[row+1][col+1]
            if region != '.':
                borders = follow(row+1, col+1, maze, region)
                area = clean(maze)
                multiplier = sides(borders) if discount else len(borders)
                prices.append(area * multiplier)
    return prices

def follow(x, y, maze, region):
    maze[x][y] = ','
    fences = []        
    for dx, dy in DIRECTIONS:
        nxt = maze[x+dx][y+dy]
        if nxt != ',' and nxt != region:
            fences.append(((x, y), (x+dx, y+dy)))
        elif nxt == region:
            fences.extend(follow(x+dx, y+dy, maze, region))
    return fences

def sides(borders):
    x = defaultdict(list)
    y = defaultdict(list)
    # aggregate rows and cols of the fences, but taking care to distinguish walls
    # seen from "the inside" or "the outside", to avoid the problem with maze 5
    for (ax, ay), (bx, by) in borders:
        if ax == bx:
            y[(ay, min(ay, by))].append(ax)
        if ay == by:
            x[(ax, min(ax, bx))].append(ay)

    # Once listed, doesn't matter if wall is hor or vert. But walls need to be contiguous!
    segments = [sorted(s) for s in x.values()] + [sorted(s) for s in y.values()]
    count = 0
    for segment in segments:
        last = -2
        for this in segment:
            if this != last + 1:
                count += 1
            last = this
    return count

def plot(maze):
    for row in maze:
        print(''.join([str(c) for c in row]))

def clean(maze):
    area = 0
    for row in maze:
        for j, col in enumerate(row):
            if row[j] == ',':
                row[j] = '.'
                area += 1
    return area

def read_lines(filename):
    maze = []
    with open(filename) as lines:
        for line in lines:
            maze.append(['.'] + [p for p in line.strip()] + ['.'])
    border = ['.' for i in range(len(maze[0]))]
    maze.insert(0, border)
    maze.append(border[:])
    return maze

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
