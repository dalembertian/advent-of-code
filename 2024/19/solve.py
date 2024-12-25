#!/usr/bin/env python
# encoding: utf-8

from argparse import ArgumentParser
from collections import defaultdict, deque
from re import compile

def main(args):
    designs, patterns = read_lines(args.filename)
    # print(designs)
    # print(patterns)
    # print()

    print(f'Part 1 - {[search_for_pattern(pattern, designs) for pattern in patterns].count(1)} designs are possible.')

    # for pattern in patterns:
    #     if search_for_pattern(pattern, designs):
    #         print(f'{pattern} can be done in {search_for_pattern(pattern, designs, count=True)}')

    print(f'Part 2 - different ways to make designs: {sum([search_for_pattern(pattern, designs, count=True) for pattern in patterns])}')

def search_for_pattern(pattern, designs, count=False):
    length = len(pattern)
    success = 0

    # print(pattern)
    attempts = deque([(design, 0) for design in designs[pattern[0]] if pattern.startswith(design)])
    while attempts:
        # if count:
        #     print(attempts)
        design, index = attempts.popleft()
        i = 0
        while i < len(design):
            if index + i == length or design[i] != pattern[index + i]:
                break
            i += 1
        if i == len(design):
            if index + i == length:
                if count:
                    success += 1
                    # print(f'success :{success}!')
                    while attempts and attempts[0][0][0] == pattern[index]:
                        attempts.popleft()
                else:
                    return 1
            else:
                j = index + i
                attempts.extendleft([(design, j) for design in designs[pattern[j]] if pattern[j:].startswith(design) and len(design) <= length-j])
    return success

def read_lines(filename):
    patterns = []
    designs = defaultdict(list)
    with open(filename) as input:
        raw_designs = [design.strip() for design in input.readline().strip().split(',')]
        for design in raw_designs:
            designs[design[0]].append(design)
        for k, v in designs.items():
            v.sort(key=lambda e: len(e), reverse=True)

        input.readline()
        for line in input.readlines():
            patterns.append(line.strip())
    return designs, patterns

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
