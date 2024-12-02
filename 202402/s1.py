#!/usr/bin/env python
# encoding: utf-8

import argparse
import collections


def main(args):
    reports, deltas = read_lines(args.filename)
    show_reports(reports, deltas)
    count_safes(deltas)

def read_lines(filename):
    reports = []
    deltas = []
    with open(filename) as lines:
        for line in lines:
            values = [int(i) for i in line.split()]
            reports.append(values)
            deltas.append([values[i+1] - values[i] for i in range(len(values) - 1)])
    return reports, deltas

def count_safes(deltas):
    safes = 0
    for delta in deltas:
        if all(1 <= i <= 3 for i in delta) or all(-3 <= i <= -1 for i in delta):
            safes += 1
    print(f'Total Reports: {len(deltas)}\n')
    print(f'Safe Reports: {safes}\n')

def show_reports(reports, deltas):
    for report, delta in zip(reports, deltas):
        safe = all(1 <= i <= 3 for i in delta) or all(-3 <= i <= -1 for i in delta)
        print(f'Safe: {safe} \t {report} \t {delta}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
