#!/usr/bin/env python
# encoding: utf-8

import argparse

def main(args):
    banks = read_lines(args.filename)

    bests = []
    for bank in banks:
        best = bank[:2]
        l = len(bank)
        for i in range(2, l):
            # print(f'{best} - {bank[i]}', end=' ')
            if i < l - 1 and bank[i] > best[0]:
                best = bank[i:i+2]
            elif bank[i] > best[1]:
                best = best[0] + bank[i]
        # print()
        # print(best)
        # print()
        bests.append(best)

    # Correct: 17435
    print(f'Part 1 - total joltage: {sum([int(x) for x in bests])}')

    # Correct:
    # print(f'Part 2 - total joltage: {}')

def invalid_id_1(id):
    # If ID has an odd length, or halves don't match, it's valid
    s = str(id)
    l = len(s)
    if l % 2 == 1 or s[:l // 2] != s[l // 2:]:
        return False
    else:
        return True

def invalid_id_2(id):
    # Assuming input has ranges with max 10-digits-long numbers
    s = str(id)
    l = len(s)

    # Test possible chunk sizes, from 1 to half the size of the string
    for k in range(l // 2, 0, -1):
        if l % k == 0:
            if s == s[:k] * (len(s) // k):
                return True
    return False

def read_lines(filename):
    with open(filename) as lines:
        return [line.strip() for line in lines]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
