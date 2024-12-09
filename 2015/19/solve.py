#!/usr/bin/env python
# encoding: utf-8
"""
https://adventofcode.com/2015/day/19
"""
import argparse


def main(args):
    subs, molecule = read_lines(args.filename)
    print(f'Molecule: {molecule}\n')
    print(f'Calibration: {len(makes_all_subs(molecule, subs))}')

    recipes = generate_molecules('e', molecule, subs)
    print(f'{len(recipes)} Recipe(s) found, minimum steps required is: {min(recipes) if recipes else None}')

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
    return subs, molecule

def makes_one_sub(molecule, substring, replacement):
    start = -1
    molecules = []
    subs = molecule.count(substring)
    for index in range(subs):
        start = molecule.find(substring, start + 1)
        molecules.append(molecule[:start] + replacement + molecule[start+len(substring):])
    return molecules

def makes_all_subs(molecule, subs):
    molecules = []
    for substring, replacement in subs:
        molecules.extend(makes_one_sub(molecule, substring, replacement))
    return set(molecules)

def generate_molecules(start, target, subs, find_all=False):
    # TODO: log the recipe steps, so the molecule can be reproduced! :-)
    recipes = []
    target_size = len(target)

    level = (start)
    level_number = 1
    while level:
        new_level = []
        for m in level:
            new_molecules = makes_all_subs(m, subs)
            for new_m in new_molecules:
                if new_m == target:
                    recipes.append(level_number)
                    if not find_all:
                        return recipes
                elif len(new_m) < target_size:
                    new_level.append(new_m)
        level = set(new_level)
        level_number += 1
        # print(level_number)
        # print([level])

    return recipes

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
