#!/usr/bin/env python
# encoding: utf-8

import argparse
import re

from collections import namedtuple, defaultdict
from itertools import combinations 
from functools import reduce


Machine = namedtuple('Machine', ['goal', 'buttons', 'joltage'])


def main(args):
    machines = read_lines(args.filename)
    sequences = find_best_sequence(machines)

    # Correct: 532
    print(f'Part 1 - fewest presses: {sum(len(s) for s in sequences)}')
    

def find_best_sequence(machines):
    sequences = []
    for machine in machines:
        outputs = defaultdict(list)
        combos = [list(combinations(machine.buttons, length)) for length in range(1, len(machine.buttons) + 1)]
        combos = [list(sublist) for g in combos for sublist in g]  
        for combo in combos:
            output = reduce(lambda x, y: x ^ y, combo)
            if len(outputs[output]) == 0 or len(outputs[output]) > len(combo):
                outputs[output].clear()
                outputs[output].extend(combo)
        sequences.append(outputs[machine.goal])
    return sequences


def read_lines(filename):
    g = re.compile(r'\[.+\]')
    b = re.compile(r'\([\d\,]+\)')
    j = re.compile(r'\{.+\}')
    machines = []
    with open(filename) as lines:
        for line in lines:
            goal = int(g.findall(line)[0][1:-1].replace('.', '0').replace('#', '1')[::-1], 2)
            buttons = [sum(2**int(digit) for digit in button[1:-1].split(',')) for button in b.findall(line)]
            joltage = [int(jolt) for jolt in j.findall(line)[0][1:-1].split(',')]
            machines.append(Machine(goal, buttons, joltage))
    return machines


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
