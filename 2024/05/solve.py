#!/usr/bin/env python
# encoding: utf-8

import argparse
import re


def main(args):
    rules, pages = read_lines(args.filename)

    correct_sum, incorrect_pages = check_pages(pages, rules)
    print(f'Part 1 - correct pages sum is: {correct_sum}, incorrect pages remaining: {len(incorrect_pages)}')

    corrected_pages = fix_pages(incorrect_pages, rules)
    correct_sum, incorrect_pages = check_pages(corrected_pages, rules)
    print(f'Part 2 - correctED pages sum is: {correct_sum}, incorrect pages remaining: {len(incorrect_pages)}')

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

def check_pages(pages, rules):
    correct_sum = 0
    incorrect_pages = []
    for page in pages:
        page_sum = check_page(page, rules)
        if page_sum:
            correct_sum += page_sum
        else:
            incorrect_pages.append(page)
    return correct_sum, incorrect_pages

def check_page(page, rules, fix=False):
    pairs = generate_pairs(page)
    for i, j in pairs:
        for rule in rules.get(i, []):
            if j in rule:
                if fix:
                    k, v = page.index(i), page.index(j)
                    page[k], page[v] = page[v], page[k]
                return 0
    return int(page[len(page)//2])

def generate_pairs(page):
    pairs = []
    for i in range(len(page)-1):
        pairs.extend([ (page[i], j) for j in page[i+1:] ])
    return pairs

def fix_pages(pages, rules):
    return [fix_page(page, rules) for page in pages]

def fix_page(page, rules):
    while not check_page(page, rules, fix=True):
        pass
    return page

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
