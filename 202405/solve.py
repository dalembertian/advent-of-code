#!/usr/bin/env python
# encoding: utf-8

import argparse
import re


def main(args):
    rules, pages = read_lines(args.filename)
    # print(rules)
    # print(pages)

    print(f'Part 1 - correct pages sum is: {sum(check_page(page, rules) for page in pages)}')

def read_lines(filename):
    rules = {}
    pages = []
    with open(filename) as lines:
        for line in lines:
            if '|' in line:
                # inverted rules
                v, k = line.strip().split('|')
                values = rules.setdefault(k, [])
                values.append(v)
                rules[k] = values
            elif ',' in line:
                pages.append(line.strip().split(','))
    return rules, pages

def check_page(page, rules):
    pairs = generate_pairs(page)
    for i, j in pairs:
        for rule in rules.get(i, []):
            if j in rule:
                return 0
    return int(page[len(page)//2])

def generate_pairs(page):
    pairs = []
    for i in range(len(page)-1):
        pairs.extend([ (page[i], j) for j in page[i+1:] ])
    return pairs

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
