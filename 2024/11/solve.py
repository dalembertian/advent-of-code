#!/usr/bin/env python
# encoding: utf-8

import argparse
from math import log10

cache = {}

def main(args):
    line = read_lines(args.filename)
    blinks = int(args.blinks)
    print(line)

    # new_line = change_stones(line, blinks)
    # print(f'Amount of stones after {blinks} blinks: {len(new_line)}')

    # total = 0
    # for sub in line:
    #     total += len(change_stones([sub], blinks))
    # print(f'Amount of stones after {blinks} blinks: {total}')

    stones = sum([change_stones_recursively(stone, blinks) for stone in line])
    print(f'Amount of stones after {blinks} blinks: {stones}')

def change_stones(line, times=1):
    for i in range(times):
        print(i)
        new_line = []
        for stone in line:
            if stone == 0:
                new_line.append(1)
            else:
                digits = int(log10(stone)) + 1
                # print(stone, digits)
                if digits % 2 == 0:
                    power = 10 ** (digits // 2)
                    left  = stone // power
                    right = stone % power
                    # right = stone % power - left
                    # print(stone, left, right)
                    new_line.append(left)
                    new_line.append(right)
                else:
                    new_line.append(2024 * stone)
        line = new_line
        # print(line)
    return line

def change_stones_recursively(stone, times, turn=0):
    if turn == times:
        return 1
    total = 0
    if stone == 0:
        total += change_stones_recursively(1, times, turn+1)
    else:
        left, right = split_stone(stone)
        total += change_stones_recursively(left, times, turn+1)
        if right >= 0:
            total += change_stones_recursively(right, times, turn+1)
    return total

def split_stone(stone):
    digits = int(log10(stone)) + 1
    if digits % 2 == 0:
        power = 10 ** (digits // 2)
        left  = stone // power
        right = stone % power
        return (left, right)
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
