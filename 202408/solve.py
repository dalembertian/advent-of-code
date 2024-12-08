#!/usr/bin/env python
# encoding: utf-8

import argparse


def main(args):
    antennas, length, width = read_lines(args.filename)

    antinodes = set(count_antinodes(antennas, length, width))
    print(f'Part 1 - total (unique) antinodes: {len(antinodes)}')

    plot(antennas, antinodes, length, width)

def count_antinodes(antennas, length, width):
    antinodes = []
    for frequency, positions in antennas.items():
        for i, a in enumerate(positions[:-1]):
            for b in positions[i+1:]:
                dx, dy = b[0] - a[0], b[1] - a[1]
                nodes = [(a[0]-dx, a[1]-dy), (b[0]+dx, b[1]+dy)]
                antinodes.extend([n for n in nodes if 0 <= n[0] < length and 0 <= n[1] < width])
    return antinodes

def plot(antennas, antinodes, length, width):
    grid = [['.' for j in range(width)] for i in range(length)]
    for f, pos in antennas.items():
        for p in pos:
            grid[p[0]][p[1]] = f
    for p in antinodes:
        grid[p[0]][p[1]] = '#'
    for row in grid:
        print(''.join(row))

def read_lines(filename):
    antennas = {}
    with open(filename) as lines:
        for i, line in enumerate(lines):
            for j, char in enumerate(line.strip()):
                if char != '.':
                    antennas.setdefault(char, []).append((i,j))
    return antennas, i+1, j+1

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
