#!/usr/bin/env python
# encoding: utf-8

import argparse


def main(args):
    subs, molecule = read_lines(args.filename)
    print(f'Molecule: {molecule}\n')
    print(f'Calibration: {len(calibrate(molecule, subs))}')

def read_lines(filename):
    # subs = {}
    subs = []
    with open(filename) as lines:
        for line in lines:
            if line.find(' => ') > 0:
                k, v = line.strip().split(' => ')
                # values = subs.setdefault(k, [])
                # values.append(v)
                subs.append((k,v))
            else:
                break
        molecule = lines.readline().strip()
    print(subs)
    return subs, molecule

def sub(molecule, substring, replacement):
    start = -1
    molecules = []
    subs = molecule.count(substring)
    for index in range(subs):
        start = molecule.find(substring, start + 1)
        molecules.append(molecule[:start] + replacement + molecule[start+len(substring):])
    return molecules

def calibrate(molecule, subs):
    molecules = []
    for substring, replacement in subs:
        molecules.extend(sub(molecule, substring, replacement))
    return set(molecules)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
