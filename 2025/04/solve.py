#!/usr/bin/env python
# encoding: utf-8

import argparse


def main(args):
    rows = read_lines(args.filename)

    # Correct: 1384
    total = check_accessibles(rows)
    print(f'Part 1 - accessible rolls: {total}')

    # Correct: 8013
    iterations = 1
    while accessibles := check_accessibles(rows):
        total += accessibles
        iterations += 1
    print(f'Part 2 - total accessible rolls (after {iterations} iterations): {total}')


def check_accessibles(rows):
    accessibles = []
    for i in range(1, len(rows) -1):
        for j in range(1, len(rows[i]) - 1):
            if accessible(rows, i, j):
                accessibles.append((i,j))
    for i, j in accessibles:
        rows[i][j] = '.'
    return len(accessibles)


def accessible(rows, i, j):
    if rows[i][j] != '@':
        return False
    blocks = 0
    for k in range(-1, 2):
        for l in range(-1, 2):
            if (k != 0 or l != 0) and rows[i+k][j+l] == '@':
                blocks += 1
                if blocks > 3:
                    return False
    return True


def read_lines(filename):
    rows = []
    with open(filename) as lines:
        for line in lines:
            rows.append(list('.'+line.strip()+'.'))
    boundary = '.' * len(rows[1])
    rows.insert(0, list(boundary))
    rows.append(list(boundary))
    return rows


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
