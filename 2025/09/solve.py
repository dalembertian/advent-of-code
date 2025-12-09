#!/usr/bin/env python
# encoding: utf-8

import argparse

from collections import namedtuple

Coord = namedtuple('Coord', ['x', 'y'])
Area = namedtuple('Area', ['first', 'second', 'area'])

def main(args):
    tiles = read_lines(args.filename)
    areas = calculate_areas(tiles)

    # Correct: 4759531084
    print(f'Part 1 - largest area: {areas[0].area}')


def calculate_areas(tiles):
    areas = []
    num_tiles = len(tiles)
    for i in range(num_tiles):
        for j in range(i+1, num_tiles):
            a, b = tiles[i], tiles[j]
            areas.append(Area(a, b, abs((a.x - b.x + 1) * (a.y - b.y + 1))))

    # All pairs of tiles, ordered from largest to smallest area
    areas.sort(key=lambda a: a.area, reverse=True)
    return areas


def read_lines(filename):
    with open(filename) as lines:
        return [Coord(int(a), int(b)) for a, b in (line.split(',') for line in lines)]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
