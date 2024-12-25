#!/usr/bin/env python
# encoding: utf-8

import argparse
import re

from keypads import *

# x, y, next
MOVEMENTS = {
    '^': (-1,  0, '>'),
    '>': ( 0,  1, 'v'),
    'v': ( 1,  0, '<'),
    '<': ( 0, -1, '^'),
}

def main(args):
    door_codes = read_lines(args.filename)
    setup_keypads()
    # for k in sorted(NUM_KEYPAD.keys()):
    #     print(k, NUM_KEYPAD[k])
    # print(NUM_BLOCKS)

    # 185256 - too high
    total = 0
    for code in door_codes:
        r1 = num_keypad_strokes(code)
        r2 = dir_keypad_strokes(r1)
        r3 = dir_keypad_strokes(r2)
        code_num = int(re.search(r'(\d+)A*', code).group(1))
        code_len = len(r3)
        complexity = code_num * code_len
        total += complexity
        print(f'code: {code} - {code_num:5} x {code_len:3} = {complexity:8} {''.join(r3)}')
    print()
    print(f'Part 1 - Complexity: {total}')

def num_keypad_strokes(code):
    # print(code)
    start = 'A'
    strokes = []
    for symbol in code:
        keys = NUM_KEYPAD[(start, symbol)]
        if keys:
            strokes.extend(keys)
        strokes.append('A')
        # print(strokes)
        start = symbol
    # print()
    return strokes

def dir_keypad_strokes(code):
    # print(code)
    start = 'A'
    strokes = []
    for symbol in code:
        keys = DIR_KEYPAD[(start, symbol)]
        if keys:
            strokes.extend(keys)
        strokes.append('A')
        # print(strokes)
        start = symbol
    # print()
    return strokes

def read_lines(filename):
    with open(filename) as input:
        return [line.strip() for line in input.readlines()]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
