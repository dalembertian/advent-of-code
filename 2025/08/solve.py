#!/usr/bin/env python
# encoding: utf-8

import argparse

from functools import reduce
from math import sqrt


def main(args):
    boxes = read_lines(args.filename)
    distances = calculate_distances(boxes)

    # Correct: 121770
    circuits, last = make_circuits(1000, boxes, distances)
    length = estimate_length(3, circuits)
    print(f'Part 1 - estimation: {length}')

    # Correct: 7893123992
    circuits, (a, b, d) = make_circuits(1000, boxes, distances, True)
    x1, x2 = boxes[a][0], boxes[b][0]
    print(f'Part 2 - estimation: {x1 * x2}')


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

    # All pairs of boxes, ordered from smallest to largest distance
    distances.sort(key=lambda x: x[2])
    return distances


def make_circuits(n, boxes, distances, complete = False):
    circuits = []
    for i, distance in enumerate(distances):
        a, b, d = distance
        added_to = []

        # Check each existing circuit for this pair of boxes
        for j, c in enumerate(circuits):
            if a in c or b in c:
                c.update([a, b])
                added_to.append(j)

        if len(added_to) == 0:
            # If no existing circuit had these boxes yet, just add them
            circuits.append(set([a,b]))

        elif len(added_to) > 1:
            # If boxes were added to TWO circuits, that means we can join them together
            circuits[added_to[0]].update(circuits.pop(added_to[1]))

        # Stop if either limit is reached or when there's only ONE circuit to rule them all...
        if (complete and len(circuits) == 1 and len(circuits[0]) == len(boxes)) or (not complete and i == n - 1):
            break

    # Circuits formed, from largest to smallest
    circuits.sort(key=lambda x: len(x), reverse=True)
    return circuits, distance # last pair of boxes added


def read_lines(filename):
    with open(filename) as lines:
        return [(int(a), int(b), int(c)) for a, b, c in [line.split(',') for line in lines.readlines()]]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
