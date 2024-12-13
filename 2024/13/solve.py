#!/usr/bin/env python
# encoding: utf-8

import argparse
import re
        
def main(args):
    machines = read_lines(args.filename)

    prizes = get_prizes(machines)
    print(f'Part 1 - Total amount of tokens to win {len(prizes)} prizes is: {sum(prizes)}')

    increase_distance(machines)
    prizes = get_prizes(machines)
    print(f'Part 2 - Total amount of tokens to win {len(prizes)} prizes is: {sum(prizes)}')

def get_prizes(machines):
    prizes = [solve_equation(machine) for machine in machines]
    return [3*p[0] + p[1] for p in prizes if p]

def solve_equation(machine):
    # Tricky explanation for the problem - we don't need to look for the BEST
    # solution, there's only ONE solution for each machine! >:-(
    # Looking for (a,b) such that a*x + b*y = p (system of 2 equations)
    (ax, ay), (bx, by), (px, py) = machine
    a = (px * by - py * bx) / (ax * by - ay * bx)
    b = (px - a * ax) / bx
    return (int(a), int(b)) if a.is_integer() and b.is_integer() else None

def increase_distance(machines):
    for i, machine in enumerate(machines):
        a, b, (px, py) = machine
        machines[i] = (a, b, (px + 10000000000000, py + 10000000000000))

def read_lines(filename):
    values = re.compile(r'.*X[+|=](\d+), Y[+|=](\d+)')
    machines = []
    with open(filename) as input:
        lines = input.readlines()
    lines.insert(0, '')
    while lines:
        lines.pop(0)
        machines.append((
            tuple([int(e) for e in values.search(lines.pop(0)).groups()]),
            tuple([int(e) for e in values.search(lines.pop(0)).groups()]),
            tuple([int(e) for e in values.search(lines.pop(0)).groups()]),
        ))
    return machines

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
