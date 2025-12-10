#!/usr/bin/env python
# encoding: utf-8

import argparse
import re
import z3

from collections import namedtuple, defaultdict
from itertools import combinations 
from functools import reduce


Machine = namedtuple('Machine', ['goal', 'buttons', 'joltage'])


def main(args):
    machines = read_lines(args.filename)

    # Correct: 532
    sequences = find_best_for_goal(machines)
    print(f'Part 1 - fewest presses for goals: {sum(sequences)}')

    # Correct: 18387
    sequences = find_best_for_joltage(machines)
    print(f'Part 2 - fewest presses for joltages: {sum(sequences)}')


def find_best_for_joltage(machines):
    # from @jonathanpaulson5053
    # brew install z3
    # pip install z3-solver
    sequences = []
    for machine in machines:
        B = [z3.Int(f'B{i}') for i in range(len(machine.buttons))]
        EQ = []
        for i in range(len(machine.joltage)):
            terms = []
            for j in range(len(machine.buttons)):
                if machine.buttons[j] & 2**i:
                    terms.append(B[j])
            eq = (sum(terms) == machine.joltage[i])
            EQ.append(eq)
        o = z3.Optimize()
        o.minimize(sum(B))
        for eq in EQ:
            o.add(eq)
        for b in B:
            o.add(b >= 0)
        assert o.check()
        M = o.model()
        for d in M.decls():
            # print(d.name(), M[d])
            sequences.append(M[d].as_long())
    return sequences


def find_best_for_goal(machines):
    # Insight: pressing a button twice makes no difference, so all we need to consider is all possible
    # combinations of buttons, pressed once or none.
    sequences = []
    for machine in machines:
        outputs = defaultdict(int)
        combos = [list(combinations(machine.buttons, length)) for length in range(1, len(machine.buttons) + 1)]
        # TODO: really weird list comprehension to flatten out a list of lists
        combos = [list(sublist) for g in combos for sublist in g]  
        for combo in combos:
            output = reduce(lambda x, y: x ^ y, combo)
            if outputs[output] == 0 or outputs[output] > len(combo):
                outputs[output] = len(combo)
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
