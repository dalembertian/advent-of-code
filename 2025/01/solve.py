#!/usr/bin/env python
# encoding: utf-8

import argparse

def main(args):
    turns = read_lines(args.filename)

    position = 50
    zeroes = passes = 0

    for turn in turns:
        value = int(turn[1:])

        # Each 100 turns is already a pass, we can count and remove them
        passes += value // 100
        value %= 100
        value = value if turn[0] == 'R' else -value

        # Don't count if starting at zero!
        new_position = position + value
        if position > 0 and (new_position < 0 or new_position > 100):
            passes += 1

        # Did it END at zero?
        position = new_position % 100
        if position == 0:
            zeroes += 1

    print(f'Part 1 - zeroes: {zeroes}')
    print(f'Part 2 - passes: {passes} -> total is {passes + zeroes}')

def read_lines(filename):
    with open(filename) as lines:
        return [line.strip() for line in lines]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
