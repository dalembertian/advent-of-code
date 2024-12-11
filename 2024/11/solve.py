#!/usr/bin/env python
# encoding: utf-8

import argparse

def main(args):
    line = read_lines(args.filename)
    blinks = int(args.blinks)
    print(line)

    new_line = change_stones(line, blinks)
    print(f'Amount of stones after {blinks} blinks: {len(new_line)}')

def change_stones(line, times=1):
    for i in range(times):
        # print(i)
        new_line = []
        for stone in line:
            if stone == '0':
                new_line.append('1')
            elif len(stone) % 2 == 0:
                l = len(stone)
                new_line.append(str(int(stone[:l // 2])))
                new_line.append(str(int(stone[l // 2:])))
            else:
                new_line.append(str(2024 * int(stone)))
        line = new_line
    return line

def read_lines(filename):
    with open(filename) as lines:
        return [stone for stone in lines.readline().strip().split()]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    parser.add_argument("blinks", help='Amount of blinks ;-)')
    args = parser.parse_args()
    main(args)
