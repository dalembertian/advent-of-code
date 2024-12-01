#!/usr/bin/env python
# encoding: utf-8

import argparse
import collections


def main(args):
    a, b = get_lists(args.filename)
    distance(a, b)
    similarity(a, b)

def get_lists(filename):
    a = []
    b = []
    with open(filename) as lines:
        for line in lines:
            col1, col2 = line.split()
            a.append(int(col1))
            b.append(int(col2))
    print(f'Lines read: {len(a)}\n')
    return sorted(a), sorted(b)

def distance(a, b):
    distance = sum(abs(i - j) for i, j in zip(a, b))
    print(f'Distance is {distance}\n')

def similarity(a, b):
    a_count = collections.Counter(a)
    b_count = collections.Counter(b)

    # Out of curiosity, how many duplicates are there in each list?
    print('Duplicates: %d %d\n' % (
        sum(count for count in a_count.values() if count > 1),
        sum(count for count in b_count.values() if count > 1)
    ))

    similarity = sum(i * b_count[i] for i in a)
    print(f'Similarity is {similarity}\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
