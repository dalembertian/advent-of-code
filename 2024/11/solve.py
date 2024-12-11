#!/usr/bin/env python
# encoding: utf-8

import argparse
from functools import cache

from math import log10

def main(args):
    line = read_lines(args.filename)
    # blinks = int(args.blinks)
    # print(line)

    for part, blinks in ((1, 25), (2, 75)):
        stones = sum([change_stones(stone, blinks) for stone in line])
        print(f'Part {part} - Amount of stones after {blinks} blinks: {stones}')

@cache
def change_stones(stone, times):
    if times == 0:
        return 1
    total = 0
    if stone == 0:
        total += change_stones(1, times - 1)
    else:
        left, right = split_stone(stone)
        total += change_stones(left, times - 1)
        if right >= 0:
            total += change_stones(right, times - 1)
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
    # parser.add_argument("blinks", help='Amount of blinks ;-)')
    args = parser.parse_args()
    main(args)
