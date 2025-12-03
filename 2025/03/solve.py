#!/usr/bin/env python
# encoding: utf-8

import argparse

def main(args):
    banks = read_lines(args.filename)

    # Correct: 17435
    print(f'Part 1 - total joltage: {sum([int(x) for x in find_bests(banks, 2)])}')

    # Correct: 172886048065379
    print(f'Part 2 - total joltage: {sum([int(x) for x in find_bests(banks, 12)])}')

def find_bests(banks, size):
    bests = []
    for bank in banks:
        best = bank[:size]
        last_considered = 0
        for i in range(1, len(bank)):
            # if there's not enough batteries left
            first_possible_digit = max(0, size - len(bank) + i)
            # if a battery has just been replaced
            last_possible_digit = min(last_considered, size - 1)
            for j in range(first_possible_digit, last_possible_digit + 1):
                if best[j] < bank[i]:
                    best = best[:j] + bank[i:i+size-j]
                    last_considered = j
                    break
            last_considered += 1
        bests.append(best)
    return bests

def read_lines(filename):
    with open(filename) as lines:
        return [line.strip() for line in lines]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
