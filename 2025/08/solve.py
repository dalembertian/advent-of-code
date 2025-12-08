#!/usr/bin/env python
# encoding: utf-8

import argparse

from functools import reduce
from math import sqrt


def main(args):
    boxes     = read_lines(args.filename)
    distances = calculate_distances(boxes)
    circuits  = make_circuits(1000, distances)
    length    = estimate_length(3, circuits)

    # Correct: 121770
    print(f'Part 1 - estimation: {length}')


def estimate_length(n, circuits):
    return reduce(lambda x, y: x * y, [len(c) for c in circuits[:n]])


def calculate_distances(boxes):
    distances = []
    num_boxes = len(boxes)
    for i in range(num_boxes):
        for j in range(i+1, num_boxes):
            a, b, c = boxes[i]
            d, e, f = boxes[j]
            distances.append((i, j, sqrt((a-d)**2 + (b-e)**2 + (c-f)**2)))
    distances.sort(key=lambda x: x[2])
    return distances


def make_circuits(n, distances):
    circuits = []
    for i in range(n):
        a, b, d = distances[i]
        # print(f'({a:3},{b:3}) ', end=' ')
        added_to = []
        for j, c in enumerate(circuits):
            if a in c or b in c:
                c.update([a, b])
                added_to.append(j)
        if len(added_to) == 0:
            circuits.append(set([a,b]))
        elif len(added_to) > 1:
            circuits[added_to[0]].update(circuits.pop(added_to[1]))
        # print(f' {len(circuits):2} {circuits}')
    circuits.sort(key=lambda x: len(x), reverse=True)
    return circuits


def read_lines(filename):
    with open(filename) as lines:
        return [(int(a), int(b), int(c)) for a, b, c in [line.split(',') for line in lines.readlines()]]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
