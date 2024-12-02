#!/usr/bin/env python
# encoding: utf-8

import argparse


def main(args):
    reports, deltas = read_lines(args.filename)
    # show_reports(reports, deltas)
    count_safes(deltas)

    dampen_reports(reports, deltas)
    # show_reports(reports, deltas)
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
    safes = [is_safe(delta) for delta in deltas].count(True)
    print(f'Total Reports: {len(deltas)}')
    print(f'Safe Reports: {safes}\n')

def dampen_reports(reports, deltas):
    # This could be made more efficient by disconsidering reports that have 2+ problems in their deltas
    # (that is, 0s or just one different sign), since those can NEVER be fixed. Out of the ones that
    # have just ONE problem, there's a chance (still not guaranteed)
    # Also, there's probably many ways to improve efficiency by analyzing the delta instead of trying
    # by brute force: adding pairs, for instance, might work.
    for index, (report, delta) in enumerate(zip(reports, deltas)):
        if not is_safe(delta):
            show_reports([report], [delta])
            for i in range(len(report)):
                new_report = list(report)
                new_report.pop(i)
                new_delta = [new_report[i+1] - new_report[i] for i in range(len(new_report) - 1)]
                if is_safe(new_delta):
                    show_reports([new_report], [new_delta])
                    reports[index] = new_report
                    deltas[index] = new_delta
                    break
            print()

def show_reports(reports, deltas):
    for report, delta in zip(reports, deltas):
        print(f'Safe: {is_safe(delta)} \t {report} \t {delta}')

def is_safe(delta):
    return all(1 <= i <= 3 for i in delta) or all(-3 <= i <= -1 for i in delta)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
