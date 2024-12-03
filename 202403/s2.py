#!/usr/bin/env python
# encoding: utf-8

import argparse
import re


def main(args):
    lines = read_lines(args.filename)
    print(f'Part 1 - Sum of mul()\'s is: {add_muls(find_muls(lines))}')
    print(f'Part 2 - Sum of VALID mul()\'s is: {add_muls(find_valid_muls(lines))}')

def read_lines(filename):
    with open(filename) as lines:
        return [line.strip() for line in lines]

def find_muls(lines):
    multiply = re.compile(r'mul\((\d{1,3}),(\d{1,3})\)')

    muls = []
    for line in lines:
        muls.extend((int(i),int(j)) for i,j in multiply.findall(line))
    return muls

def find_valid_muls(lines):
    multiply = re.compile(r'mul\((\d{1,3}),(\d{1,3})\)|(do\(\))|(don\'t\(\))')

    valid = True
    valid_muls = []
    for line in lines:
        muls = multiply.findall(line)
        for a,b,do,dont in muls:
            if valid and a and b:
                valid_muls.append((int(a), int(b)))
            elif do:
                valid = True
            elif dont:
                valid = False
    return valid_muls

def add_muls(muls):
    return sum(i*j for i,j in muls)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
