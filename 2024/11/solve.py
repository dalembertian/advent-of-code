#!/usr/bin/env python
# encoding: utf-8

import argparse
from math import log10

cache = {}

def main(args):
    line = read_lines(args.filename)
    blinks = int(args.blinks)
    print(line)

    stones = sum([change_stones(stone, blinks) for stone in line])
    print(f'Amount of stones after {blinks} blinks: {stones}')

def change_stones(stone, times, turn=0):
    if turn == times:
        return 1
    total = 0
    if stone == 0:
        total += change_stones(1, times, turn+1)
    else:
        total += change_stones(left, times, turn+1)
        if right >= 0:
            total += change_stones(right, times, turn+1)
    return total

def split_stone(stone):
    digits = int(log10(stone)) + 1
    if digits % 2 == 0:
        power = 10 ** (digits // 2)
        return (stone // power, stone % power)
    else:
        return (2024 * stone, -1)

def read_lines(filename):
    with open(filename) as lines:
        return [int(stone) for stone in lines.readline().strip().split()]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    parser.add_argument("blinks", help='Amount of blinks ;-)')
    args = parser.parse_args()
    main(args)
