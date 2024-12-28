#!/usr/bin/env python
# encoding: utf-8

import argparse
import re


def main(args):
    lcks, keys = read_lines(args.filename)
    print(lcks)
    print(keys)

def read_lines(filename):
    lck = re.compile(r'(#+)(\.+)')
    key = re.compile(r'(\.+)(#+)')
    lcks = []
    keys = []
    with open(filename) as input:
        lines = input.readlines()
    for i in range(0, len(lines), 8):
        piece = [line.strip() for line in lines[i:i+7]]
        sided = [''.join([line[i] for line in piece]) for i in range(5)]
        if sided[0][0] == '#':
            lcks.append([len(lck.search(pin).group(1))-1 for pin in sided])
        else:
            keys.append([len(key.search(pin).group(1))-1 for pin in sided])
    return lcks, keys

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
