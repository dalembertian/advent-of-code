#!/usr/bin/env python
# encoding: utf-8

import argparse
import re

from collections import defaultdict

AND = lambda a, b: a & b
OR  = lambda a, b: a | b
XOR = lambda a, b: a ^ b
NUL = lambda a, b: a
OPS = {
    'AND': AND,
    'OR': OR,
    'XOR': XOR,
    'NUL': NUL,
}

def main(args):
    operats, results, tests = read_lines(args.filename)

    zb, zd = run(operats, results)
    # show_xyz(results)
    print(f'Part 1 - Z values form the binary number {zb}, or decimal: {zd}')

    # check_adder(operats)
    pairs = swap_gates(args)
    wires = ','.join(sorted(','.join([f'{i},{j}' for i, j in pairs]).split(',')))
    print(f'Part 2 - wires that need to be switched for the adder to work: {wires}')

def check_adder(operats):
    depends, is_deps = create_graph(operats)

    # Digit 0
    is_deps['x00'].clear()
    is_deps['y00'].remove('z00')
    carry_in = is_deps['y00'].pop()

    for digit in range(1, 45):
        try:
            x, y, z = f'x{digit:02}', f'y{digit:02}', f'z{digit:02}'

            # 2nd XOR
            a, b, op = operats[z]
            assert op == 'XOR', f'carry_in: {carry_in}, {z} = carry_in {a} XOR ({op}) first_xor {b}'
            assert a != x and a != y and b != x and b != y, f'{z} = carry-in ({a}) XOR ({op}) first_xor ({b})'

            # one of z's entries is the carry-in, the other is the result of an AND
            assert carry_in in (a, b), f'carry_in: {carry_in}, {carry_in} is {a} or {b}'
            is_deps[a].remove(z)
            is_deps[b].remove(z)
            assert len(is_deps[a]) == len(is_deps[b]) == 1 and is_deps[a] == is_deps[b], f'first_and'
            first_and = is_deps[a].pop()
            is_deps[b].pop()
            
            # 1st AND
            c, d, op = operats[first_and]
            assert op == 'AND', f'carry-in: {carry_in}, {first_and} = {c} first_and ({op}) {d}'
            assert c == carry_in or d == carry_in, f'first_and'
            first_xor = c if d == carry_in else d

            # 1st XOR
            e, f, op = operats[first_xor]
            assert op == 'XOR', f'{first_xor} = {e} first_xor ({op}) {f}'
            assert (e == x or e == y) and (f == x or f == y), f'first_xor ({first_xor}) = {x} XOR {y}'
            is_deps[x].remove(first_xor)
            is_deps[y].remove(first_xor)
            assert len(is_deps[x]) == len(is_deps[y]) == 1 and is_deps[x] == is_deps[y], f'first_xor'
            second_and = is_deps[x].pop()
            is_deps[y].pop()

            # 2nd AND
            g, h, op = operats[second_and]
            assert op == 'AND', f'{second_and} = {g} second_and ({op}) {h}'
            assert (g == x or g == y) and (h == x or h == y), f'second_and ({second_and}) = {x} AND {y}'

            # OR
            assert len(is_deps[first_and]) == len(is_deps[second_and]) == 1 and is_deps[first_and] == is_deps[second_and], f'OR'
            single_or = is_deps[first_and].pop()
            is_deps[second_and].pop()
            i, j, op = operats[single_or]
            assert op == 'OR', f'OR'
            assert i == first_and or i == second_and, f'{i} is {first_and} or {second_and}'
            assert j == first_and or j == second_and, f'{j} is {first_and} or {second_and}'

            carry_in = single_or
        except AssertionError as err:
            print(f'Digit: {digit}, validation error: {err}')
        except Exception as err:
            print(f'Digit: {digit}, error: {err}')            

def swap_gates(args):
    wrong = ['jqf','mdd','skh','wpd','wts','z11','z19','z37']
    wrong_pairs = create_pairs(wrong)

    for pairs in wrong_pairs:
        operats, results, tests = read_lines(args.filename)
        for pair in pairs:
            k1, k2 = pair
            operats[k1], operats[k2] = operats[k2], operats[k1]
        if test(operats, results, tests):
            return pairs

def create_pairs(list):
    if len(list) < 2:
        yield []
    else:
        a = list[0]
        for i in range(1, len(list)):
            pair = (a, list[i])
            for rest in create_pairs(list[1:i] + list[i+1:]):
                yield [pair] + rest

def input_binary(results, x=None, y=None):
    for i, b in enumerate(x[::-1]):
        results[f'x{i:02}'] = int(b)
    for i, b in enumerate(y[::-1]):
        results[f'y{i:02}'] = int(b)

def run(operats, results):
    order = solve_dependencies(operats)
    calculate(operats, results, order)
    return output('z', results)

def test(operats, results, tests):
    xs, ys, zs = tests.values()
    test_results = []
    for x, y, z in zip(xs, ys, zs):
        input_binary(results, x=x, y=y)
        zb, zd = run(operats, results)
        test_results.append(zb == z)
        # show_xyz(results, (z, int(z, 2)))
    return all(test_results)

def calculate(operats, results, order):
    for wire in order:
        a, b, op = operats[wire]
        results[wire] = OPS[op](results[a], results[b])

def show_xyz(results, expected=None):
    xb, xd = output('x', results)
    yb, yd = output('y', results)
    zb, zd = output('z', results)
    eb, ed = expected if expected else ('', 0)
    lb = max([len(xb), len(yb), len(zb), len(eb)])
    ld = max([len(str(xd)), len(str(yd)), len(str(zd)), len(str(ed))])
    print(f'x: {xb: >{lb}} ({xd:{ld}})')
    print(f'y: {yb: >{lb}} ({yd:{ld}})')
    print(f'z: {zb: >{lb}} ({zd:{ld}})')
    if expected:
        print(f'E: {eb: >{lb}} ({ed:{ld}}) {'MATCH!!!' if zb == eb else 'Not a match...'}')
    print()

def output(letter, results):
    wires = sorted([(wire, output) for wire, output in results.items() if wire[0] == letter], reverse=True)
    binary = ''.join([str(j) for i, j in wires])
    return binary, int(binary, 2)

def solve_dependencies(operats):
    depends, is_deps = create_graph(operats)
    all_nodes = set(depends.keys() | is_deps.keys())
    return kahn(all_nodes - depends.keys(), is_deps, depends)

def kahn(S, is_deps, depends):
    L = []
    while S:
        n = S.pop()
        L.append(n)
        for m in is_deps[n]:
            depends[m].remove(n)
            if not depends[m]:
                S.add(m)
    # If there are still edges in depends[], graph is cyclic
    return L

def create_graph(operats):
    depends = defaultdict(list)
    is_deps = defaultdict(list)
    for r, (a, b, op) in operats.items():
        if op != 'NUL':
            depends[r].extend([a, b])
            is_deps[a].append(r)
            is_deps[b].append(r)
    return depends, is_deps    

def show_graph(depends, is_deps, operats):
    print(f'Ops')
    for k, v in sorted(operats.items()):
        a, b, op = v
        if op != 'NUL':
            print(k, v)
    print()
    print(f'K depends on V')
    for k, v in sorted(depends.items()):
        print(k, v)
    print()
    print(f'K is a dependency for V')
    for k, v in sorted(is_deps.items()):
        print(k, v)
    print()

def read_lines(filename):
    initial = re.compile(r'^(\w+): (\d+)')
    boolean = re.compile(r'^(\w+) (AND|OR|XOR) (\w+) -> (\w+)')
    test    = re.compile(r'^(x|y|z) = ([01]+)')
    operats = {}
    results = {}
    tests   = defaultdict(list)
    with open(filename) as lines:
        for line in lines:
            if initial.search(line):
                k, v = initial.search(line).groups()
                results[k] = int(v)
                operats[k] = (k, k, 'NUL')
            if boolean.search(line):
                a, op, b, r = boolean.search(line).groups()
                operats[r] = (a, b, op)
            if test.search(line):
                k, v = test.search(line).groups()
                tests[k].append(v)
    return operats, results, tests

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
