#!/usr/bin/env python
# encoding: utf-8

import argparse
import collections


def main(args):
    a, b = get_lists(args.filename)
    print(f'Part 1 - Distance is {distance(a, b)}')
    print(f'Part 2 - Similarity is {similarity(a, b)}')

def get_lists(filename):
    a = []
    b = []
    with open(filename) as lines:
        for line in lines:
            col1, col2 = line.split()
            a.append(int(col1))
            b.append(int(col2))
    return sorted(a), sorted(b)

def distance(a, b):
    return sum(abs(i - j) for i, j in zip(a, b))

def similarity(a, b):
    a_count = collections.Counter(a)
    b_count = collections.Counter(b)

    # Out of curiosity, how many duplicates are there in each list?
    # print('Duplicates: %d %d\n' % (
    #     sum(count for count in a_count.values() if count > 1),
    #     sum(count for count in b_count.values() if count > 1)
    # ))

    return sum(i * b_count[i] for i in a)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
