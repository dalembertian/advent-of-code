#!/usr/bin/env python
# encoding: utf-8

import argparse


def main(args):
    reports = read_lines(args.filename)
    # show_reports(reports)
    count_safes(reports)

    dampen_reports(reports)
    # show_reports(reports)
    count_safes(reports)

def read_lines(filename):
    reports = []
    with open(filename) as lines:
        for line in lines:
            reports.append([int(i) for i in line.split()])
    return reports

def count_safes(reports):
    all_deltas = [calculate_deltas(report) for report in reports]
    safes = [is_safe(deltas) for deltas in all_deltas].count(True)
    print(f'Total Reports: {len(reports)}')
    print(f'Safe Reports: {safes}\n')

def dampen_reports(reports):
    # This could be made more efficient by disconsidering reports that have 2+ problems in their deltas
    # (that is, 0s or just one different sign), since those can NEVER be fixed. Out of the ones that
    # have just ONE problem, there's a chance (still not guaranteed) to fix them. Also, there's probably
    # many ways to improve efficiency by analyzing the delta instead of trying by brute force: adding pairs,
    # for instance, might work.
    for index, report in enumerate(reports):
        if not is_safe(calculate_deltas(report)):
            # show_reports([report])
            for i in range(len(report)):
                new_report = report[:i] + report[i+1:]
                if is_safe(calculate_deltas(new_report)):
                    # show_reports([new_report])
                    reports[index] = new_report
                    break
            # print()

def show_reports(reports):
    for report in reports:
        deltas = calculate_deltas(report)
        print(f'Safe: {is_safe(deltas)} \t {report} \t {deltas}')

def calculate_deltas(report):
    return [report[i+1] - report[i] for i in range(len(report)-1)]

def is_safe(deltas):
    return all(1 <= i <= 3 for i in deltas) or all(-3 <= i <= -1 for i in deltas)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
