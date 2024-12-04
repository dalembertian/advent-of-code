#!/usr/bin/env python
# encoding: utf-8

import argparse
import re


def main(args):
    lines = read_lines(args.filename)
    print(f'Part 1 - XMAS instances: {find_word("XMAS", lines)}')

def read_lines(filename):
    with open(filename) as lines:
        return [line.strip() for line in lines]

def find_word(word, lines):
    strings = [line for line in lines]
    strings.extend(generate_strings_from_columns(lines))
    strings.extend(generate_strings_from_diagonals(lines))
    strings.extend(generate_strings_from_other_diagonals(lines))

    word_regex = re.compile(word)
    count  = sum(len(word_regex.findall(string)) for string in strings)
    count += sum(len(word_regex.findall(string[::-1])) for string in strings)
    return count

def generate_strings_from_columns(lines):
    strings = []
    cols = len(lines[0])
    for col in range(cols):
        strings.append(''.join([line[col] for line in lines]))
    return strings

def generate_strings_from_diagonals(lines):
    rows = len(lines)
    cols = len(lines[0])
    matrix = [['' for j in range(cols)] for i in range(2*rows)]
    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            matrix[i+j][j] = c
    return [''.join(line) for line in matrix]

def generate_strings_from_other_diagonals(lines):
    inverted_lines = [line[::-1] for line in lines]
    return generate_strings_from_diagonals(inverted_lines)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
