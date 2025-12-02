#!/usr/bin/env python
# encoding: utf-8

import argparse

def main(args):
    ranges = read_lines(args.filename)

    invalid_ids_1 = []
    invalid_ids_2 = []
    for begin, end in ranges:
        print(f'Range: {end-begin+1:6} Max Len: {len(str(end+1)):2} ({begin}-{end})')
        for i in range(begin, end + 1):
            if invalid_id_1(i):
                invalid_ids_1.append(i)
            if invalid_id_2(i):
                invalid_ids_2.append(i)
                # print(i, end=' ')
        # print()
    print()

    # Correct: 18595663903
    print(f'Part 1 - sum of invalid IDs: {sum(invalid_ids_1)}')

    # Correct: 19058204438
    print(f'Part 2 - sum of invalid IDs: {sum(invalid_ids_2)}')

def invalid_id_1(i):
    # If ID has an odd length, or halves don't match, it's valid
    s = str(i)
    l = len(s)
    if l % 2 == 1 or s[:l // 2] != s[l // 2:]:
        return False
    else:
        return True

def invalid_id_2(i):
    # Assuming input has ranges with max 10-digits-long numbers
    s = str(i)
    l = len(s)

    if l == 1:
        return False
    if l == 10 and repetead_segments(s, 5):
        return True
    elif (l == 9 or l == 6) and repetead_segments(s, 3):
        return True
    elif l == 8 and repetead_segments(s, 4):
        return True
    if l > 2 and l % 2 == 0 and repetead_segments(s, 2):
        return True
    if repetead_segments(s, 1):
        return True
    return False

def repetead_segments(s, l):
    return s == s[:l] * (len(s) // l)

def read_lines(filename):
    with open(filename) as lines:
        line = lines.readline()
        return [(int(a), int(b)) for a,b in (id_range.split('-') for id_range in line.split(','))]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
