#!/usr/bin/env python
# encoding: utf-8

import argparse
import re


def main(args):
    lines = read_lines(args.filename)

    muls = []
    for line in lines:
        muls.extend(find_muls(line))

    print(add_muls(muls))

def read_lines(filename):
    with open(filename) as lines:
        return [line.strip() for line in lines]

def find_muls(line):
    multiply = re.compile(r'mul\((\d{1,3}),(\d{1,3})\)')
    return ((int(i),int(j)) for i,j in multiply.findall(line))

def add_muls(muls):
    return sum(i*j for i,j in muls)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
