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

    # 185256 - too high
    total = 0
    for code in door_codes:
        best_r3 = ''
        r1s = keypad_strokes(code, 'A', NUM_KEYPAD)
        for r1 in r1s:
            r2s = keypad_strokes(r1, 'A', DIR_KEYPAD)
            for r2 in r2s:
                r3s = keypad_strokes(r2, 'A', DIR_KEYPAD)
                r3s.sort(key=lambda s: len(s))
                if len(r3s[0]) < len(best_r3) or not best_r3:
                    best_r3 = r3s[0]

        code_num = int(re.search(r'(\d+)A*', code).group(1))
        code_len = len(best_r3)
        complexity = code_num * code_len
        total += complexity
        print(f'code: {code} - {code_num:5} x {code_len:3} = {complexity:8} {''.join(best_r3)}')
    print()
    print(f'Part 1 - Complexity: {total}')


def keypad_strokes(code, start, keypad):
    if code:
        options = []
        for path in keypad[(start, code[0])]:
            options.extend([path + 'A' + p for p in keypad_strokes(code[1:], code[0], keypad)])
        return options
    else:
        return ['']

def read_lines(filename):
    with open(filename) as input:
        return [line.strip() for line in input.readlines()]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
