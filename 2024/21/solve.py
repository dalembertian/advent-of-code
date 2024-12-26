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
        best = ''
        r1s = all_keypad_strokes(code, 'A', NUM_KEYPAD)
        # r1s = first_keypad_strokes(code, 'A', NUM_KEYPAD)

        # for i in range(24):
        #     r1s = first_keypad_strokes(r1s, 'A', DIR_KEYPAD)
        # r1s = [r1s]

        print(r1s)
        for i in range(0):
            r1s.sort(key=lambda s: len(s))
            r1s = [r for r in r1s if len(r) == len(r1s[0])]
            r2s = []
            for r1 in r1s:
                r2s.extend(all_keypad_strokes(r1, 'A', DIR_KEYPAD))
            r1s = r2s

        for i in range(25):
            r1s = [first_keypad_strokes(r1, 'A', DIR_KEYPAD) for r1 in r1s]
            print(i)
        r2s = r1s

        for r2 in r2s:
            if len(r2) < len(best) or not best:
                best = r2

        code_num = int(re.search(r'(\d+)A*', code).group(1))
        code_len = len(best)
        complexity = code_num * code_len
        total += complexity
        print(f'code: {code} - {code_num:5} x {code_len:3} = {complexity:8} {''.join(best)}')
    print()
    print(f'Part 1 - Complexity: {total}')

def first_keypad_strokes(code, start, keypad):
    strokes = ''
    for symbol in code:
        strokes += keypad[(start, symbol)][0]
        strokes += 'A'
        start = symbol
    return strokes

def all_keypad_strokes(code, start, keypad):
    if code:
        options = []
        for path in keypad[(start, code[0])]:
            options.extend([path + 'A' + p for p in all_keypad_strokes(code[1:], code[0], keypad)])
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
