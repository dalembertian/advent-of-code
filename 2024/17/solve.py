#!/usr/bin/env python
# encoding: utf-8

from argparse import ArgumentParser
from collections import deque
from re import compile

from computer import run

def main(args):
    program, registers = read_lines(args.filename)
    # print(f'Program: {','.join([str(o) for o in program])}')
    # print(f'Registers: {registers}')

    output = run(program, registers)
    print(f'Part 1 - Final Output: {','.join([str(o) for o in output])}')
    # print(f'Output : {','.join([str(o) for o in output])}')

    new_A = search_for_itself(program, registers)
    print(f'Part 2 - A: {new_A}')

def search_for_itself(program, registers):
    # Custom solution for input.txt (see file)
    A, B, C = registers
    target = program[::-1]
    max_digit = len(target) - 1

    attempt = deque([(0, 0)])
    while attempt:
        A, digit = attempt.popleft()
        new_A = A * 8
        while new_A < A * 8 + 8:
            output = run(program, [new_A, B, C])
            if output and output[0] == target[digit]:
                if digit == max_digit:
                    return new_A if output == program else None
                attempt.append((new_A, digit + 1))
            new_A += 1
        digit += 1

def read_lines(filename):
    values = compile(r'([\d+,?]+)')
    registers = []
    with open(filename) as input:
        for i in range(3):
            registers.append(int(values.search(input.readline()).group(0)))
        input.readline()
        program = [int(i) for i in values.search(input.readline()).group(0).split(',')]
    return program, registers

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
