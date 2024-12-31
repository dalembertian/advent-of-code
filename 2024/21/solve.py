#!/usr/bin/env python
# encoding: utf-8

import argparse
import re

from functools import reduce

from keypads import *


def main(args):
    door_codes = read_lines(args.filename)
    setup_keypads()

    print(f'Part 1 - Complexity: {run_steps(door_codes, 2)}')
    print(f'Part 2 - Complexity: {count_steps(door_codes, 25)}')

def count_steps(door_codes, robots):
    total = 0
    for code in door_codes:
        combos = all_keypad_strokes(code, 'A', NUM_KEYPAD)
        combos = [sum([count_dir_keypad_strokes(seq+'A', robots) for seq in combo.split('A')[:-1]]) for combo in combos]
        best = min(combos)
        code_num = int(re.search(r'(\d+)A*', code).group(1))
        total += code_num * best
    return total

def run_steps(door_codes, robots):
    total = 0
    for code in door_codes:
        combos = all_keypad_strokes(code, 'A', NUM_KEYPAD)
        for i in range(robots):
            # For 2 robots, both approaches work: taking the first sequence of strokes, or...
            combos = [first_keypad_strokes(combo, 'A', DIR_KEYPAD) for combo in combos]
            
            # ...looking for the best. But the latter is WAY slower.
            # combos = reduce(lambda x,y: x + y, [all_keypad_strokes(combo, 'A', DIR_KEYPAD) for combo in combos])

        best = min(combos, key=lambda c: len(c))
        code_num = int(re.search(r'(\d+)A*', code).group(1))
        total += code_num * len(best)
    return total

def read_lines(filename):
    with open(filename) as input:
        return [line.strip() for line in input.readlines()]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
