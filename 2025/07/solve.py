#!/usr/bin/env python
# encoding: utf-8

import argparse

from collections import defaultdict


def main(args):
    levels = read_lines(args.filename)

    entry = levels.pop(0)
    first_beam = entry.index('S')
    num_splits, num_timelines = count_timelines(first_beam, levels)

    # Correct: 1600
    print(f'Part 1 - splits: {num_splits}')

    # Naïve approaches (correct but exponential time)    
    # timelines = []
    # find_timelines_recursive(first_beam, levels, timelines)
    # print(f'Part 2 - timelines: {len(timelines)} or {count_timelines_recursive(first_beam, levels)}')

    # Correct: 8632253783011
    print(f'Part 2 - timelines: {num_timelines}')


def count_timelines(beam, levels):
    splits = defaultdict(int)
    splits[beam] = 1
    num_splits = 0
    for level in levels:
        new_splits = defaultdict(int)
        for beam in splits.keys():
            if level[beam] == '^':
                new_splits[beam-1] += splits[beam]
                new_splits[beam+1] += splits[beam]
                num_splits += 1
            else:
                new_splits[beam] += splits[beam]
        splits = new_splits
    return num_splits, sum(splits.values())


def count_timelines_recursive(beam, levels):
    if not levels:
        return 1
    if levels[0][beam] == '^':
        return count_timelines_recursive(beam+1, levels[1:]) + \
               count_timelines_recursive(beam-1, levels[1:])
    else:
        return count_timelines_recursive(beam, levels[1:])


def find_timelines_recursive(beam, levels, timelines, timeline = None):
    if not levels:
        timelines.append(timeline)
        return
    if not timeline:
        timeline = []
    timeline.append(beam)
    if levels[0][beam] == '^':
        find_timelines_recursive(beam+1, levels[1:], timelines, timeline[:])
        find_timelines_recursive(beam-1, levels[1:], timelines, timeline)
    else:
        find_timelines_recursive(beam, levels[1:], timelines, timeline)


def read_lines(filename):
    levels = []
    with open(filename) as lines:
        for line in lines:
            levels.append([c for c in line.strip()])
    return levels


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
