#!/usr/bin/env python
# encoding: utf-8

import argparse
import re

from collections import defaultdict


def main(args):
    shapes, trees = read_lines(args.filename)

    # It was too difficult to be true - no need to analyze the shapes at all!
    # Just checking if there's an excess of space without any nesting.
    total_fits = 0
    for (w, h), amounts in trees:
        fit_space = w // 3 * h // 3
        shapes_needed = sum(amounts)
        if fit_space >= shapes_needed:
            total_fits += 1

    print(f'Part 1 - Trees with enough space: {total_fits}')


def read_lines(filename):
    shape = re.compile(r'(\d+):')
    tree = re.compile(r'(\d+)x(\d+): (.+)')

    shapes = {}
    trees = []
    with open(filename) as lines:
        line = lines.readline()
        while match := shape.match(line):
            shapes[match.group(1)] = [lines.readline().strip() for _ in range(3)]
            lines.readline()
            line = lines.readline()
        while match := tree.match(line):
            trees.append([(int(match.group(1)), int(match.group(2))), [int(qty) for qty in match.group(3).split(' ')]])
            line = lines.readline()
    return shapes, trees


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
