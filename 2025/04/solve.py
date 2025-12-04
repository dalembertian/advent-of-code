#!/usr/bin/env python
# encoding: utf-8

import argparse

def main(args):
    rows, width = read_lines(args.filename)

    accessibles = 0
    for i in range(1, len(rows) -1):
        for j in range(1, width + 1):
            if accessible(rows, i, j):
                accessibles += 1

    # Correct: 1384
    print(f'Part 1 - accessible rolls: {accessibles}')

def accessible(rows, i, j):
    if rows[i][j] == '.':
        return False
    blocks = 0
    for k in range(-1, 2):
        for l in range(-1, 2):
            if (k != 0 or l != 0) and rows[i+k][j+l] != '.':
                blocks += 1
                if blocks > 3:
                    return False
    return True

def read_lines(filename):
    rows = []
    with open(filename) as lines:
        for line in lines:
            rows.append('.'+line.strip()+'.')
    width = len(rows[1]) - 2
    boundary = '.' * (width + 2)
    rows.insert(0, boundary)
    rows.append(boundary)
    return rows, width

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
