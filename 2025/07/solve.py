#!/usr/bin/env python
# encoding: utf-8

import argparse


def main(args):
    levels = read_lines(args.filename)

    entry = levels.pop(0)
    beams = set([entry.index('S')])
    splits = 0
    for level in levels:
        new_beams = set()
        while beams:
            beam = beams.pop()
            if level[beam] == '^':
                splits += 1
                new_beams.update([beam-1, beam+1])
            else:
                new_beams.add(beam)
        beams = new_beams
        print(beams)

    # Correct: 1600
    print(f'Part 1 - splits: {splits}')


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
