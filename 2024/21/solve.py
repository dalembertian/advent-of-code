#!/usr/bin/env python
# encoding: utf-8

import argparse
import re
import time

from keypads import *


def main(args):
    door_codes = read_lines(args.filename)
    s1, s2, s3 = args.step1, args.step2, args.step3

    setup_keypads()
    # for k in sorted(DIR_KEYPAD.keys()):
    #     print(k, DIR_KEYPAD[k])

    # print(f'Part 1 - Complexity: {run_steps(2, 0, 0, door_codes)}')

    print(f'Part 2 - Complexity: {run_steps(s1, s2, s3, door_codes)}')

def run_steps(s1, s2, s3, door_codes):
    start = time.time()
    total = 0
    for code in door_codes:
        combos = all_keypad_strokes(code, 'A', NUM_KEYPAD)
        original = combos[:]

        # Step 1 - first combination at hand
        for i in range(s1):
            print(f'Step 1, Loop {i:2}, {sum([len(combo) for combo in combos])}, t={time.time()-start:.2f}s')
            combos = [first_keypad_strokes(combo, 'A', DIR_KEYPAD) for combo in combos]

        # Step 2 - all possible combinations
        for i in range(s2):
            print(f'Step 2, Loop {i:2}, {sum([len(combo) for combo in combos])}')
            # Consider only the shortest stroke sequences
            combos.sort(key=lambda s: len(s))
            combos = [r for r in combos if len(r) == len(combos[0])]
            r2s = []
            for combo in combos:
                r2s.extend(all_keypad_strokes(combo, 'A', DIR_KEYPAD))
            combos = r2s

        # Step 3 - like Step 1, but after choosing the shortest combo so far
        if s3:
            best = min(combos, key=lambda c: len(c))
            combos = [best]
            # print(f'Best ({len(best)}): {original[combos.index(best)]}')
            for i in range(s3):
                print(f'Step 3, Loop {i:2}, {sum([len(combo) for combo in combos])}, t={time.time()-start:.2f}s')
                combos = [first_keypad_strokes(combo, 'A', DIR_KEYPAD) for combo in combos]
            print(f'Final Sizes      {[len(combo) for combo in combos]}, t={time.time()-start:.2f}s')

        best = min(combos, key=lambda c: len(c))
        code_num = int(re.search(r'(\d+)A*', code).group(1))
        code_len = len(best)
        complexity = code_num * code_len
        total += complexity
        print(f'code: {code} - {code_num:5} x {code_len:3} = {complexity:8}')
        print()
    return total

def read_lines(filename):
    with open(filename) as input:
        return [line.strip() for line in input.readlines()]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    parser.add_argument("--step1", "-s1", type=int, default=2, help='Step 1 attempts - first at hand (default: 2)')
    parser.add_argument("--step2", "-s2", type=int, default=0, help='Step 2 attempts - all possible (default: 0)')
    parser.add_argument("--step3", "-s3", type=int, default=0, help='Step 3 attempts - first at hand (default: 0)')
    args = parser.parse_args()
    main(args)
