#!/usr/bin/env python
# encoding: utf-8

from argparse import ArgumentParser
from collections import defaultdict, deque
from re import compile

def main(args):
    designs, patterns = read_lines(args.filename)
    print(designs)
    print(patterns)
    print()

    # print(f'Part 1 - {[search_for_pattern(pattern, designs) for pattern in patterns].count(True)} designs are possible.')
    for pattern in patterns:
        print(f'{pattern} is {'doable' if search_for_pattern(pattern, designs) else 'impossible'}')

def search_for_pattern(pattern, designs):
    length = len(pattern)
    print(f'pattern: {pattern}, length: {length}')

    attempts = deque([(design, 0) for design in designs[pattern[0]] if pattern.startswith(design)])
    while attempts:
        design, index = attempts.popleft()
        print(f'design: {design}, index: {index}')
        i = 0
        while i < len(design):
            # print(f'In the loop - i: {i}, index: {index}, length: {length}, design: {design}')
            if index + i == length or design[i] != pattern[index + i]:
                break
            i += 1
        # print(f'Out the loop - i: {i}, index: {index}, length: {length}, design: {design}')
        if i == len(design):
            print(f'matched design, i: {i}, index + i: {index+i} (length: {length})')
            if index + i == length:
                return True
            else:
                j = index + i
                attempts.extendleft([(design, j) for design in designs[pattern[j]]])
        else:
            print(f'no match')
        print(f'deque: {attempts}')
        input()

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
