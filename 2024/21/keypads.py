#!/usr/bin/env python
# encoding: utf-8

from functools import cache
from itertools import permutations

MOVEMENTS = {
    '^': ( 0, -1),
    '>': ( 1,  0),
    'v': ( 0,  1),
    '<': (-1,  0),
}

OPPOSITE = {
    '^': 'v',
    '>': '<',
    'v': '^',
    '<': '>',
}

"""
+---+---+---+
| 7 | 8 | 9 |
+---+---+---+
| 4 | 5 | 6 |
+---+---+---+
| 1 | 2 | 3 |
+---+---+---+
    | 0 | A |
    +---+---+
"""
NUM_KEYPAD = {
    ('0', '1'): ['^<'],
    ('0', '2'): '^',
    ('0', '3'): '^>',
    ('0', '4'): ['^^<', '^<^'],
    ('0', '5'): '^^',
    ('0', '6'): '^^>',
    ('0', '7'): ['^^^<', '^^<^', '^<^^'],
    ('0', '8'): '^^^',
    ('0', '9'): '^^^>',
    ('0', 'A'): '>',

    ('A', '1'): ['^<<', '<^<'],
    ('A', '2'): '^<',
    ('A', '3'): '^',
    ('A', '4'): ['^^<<', '^<^<', '^<<^', '<^^<', '<^<^'],
    ('A', '5'): '^^<',
    ('A', '6'): '^^',
    ('A', '7'): ['^^<<^', '^<^^<', '<^^<^', '^^<^<', '^<<^^', '^<^<^', '<^^^<', '^^^<<', '<^<^^'],
    ('A', '8'): '^^^<',
    ('A', '9'): '^^^',

    ('1', '2'): '>',
    ('1', '3'): '>>',
    ('1', '4'): '^',
    ('1', '5'): '^>',
    ('1', '6'): '^>>',
    ('1', '7'): '^^',
    ('1', '8'): '^^>',
    ('1', '9'): '^^>>',

    ('2', '3'): '>',
    ('2', '4'): '^<',
    ('2', '5'): '^',
    ('2', '6'): '^>',
    ('2', '7'): '^^<',
    ('2', '8'): '^^',
    ('2', '9'): '^^>',

    ('3', '4'): '^<<',
    ('3', '5'): '^<',
    ('3', '6'): '^',
    ('3', '7'): '^^<<',
    ('3', '8'): '^^<',
    ('3', '9'): '^^',

    ('4', '5'): '>',
    ('4', '6'): '>>',
    ('4', '7'): '^',
    ('4', '8'): '^>',
    ('4', '9'): '^>>',

    ('5', '6'): '>',
    ('5', '7'): '^<',
    ('5', '8'): '^',
    ('5', '9'): '^>',

    ('6', '7'): '^<<',
    ('6', '8'): '^<',
    ('6', '9'): '^',

    ('7', '8'): '>',
    ('7', '9'): '>>',

    ('8', '9'): '>',
}
NUM_BLOCKS = [('0', '1'), ('0', '4'), ('0', '7'), ('A', '1'), ('A', '4'), ('A', '7')]

"""
    +---+---+
    | ^ | A |
+---+---+---+
| < | v | > |
+---+---+---+
"""
DIR_KEYPAD = {
    ('<', '^'): ['>^'],
    ('<', 'A'): ['>>^', '>^>'],
    ('<', 'v'): '>',
    ('<', '>'): '>>',

    ('v', '^'): '^',
    ('v', 'A'): '>^',
    ('v', '>'): '>',

    ('>', '^'): '^<',
    ('>', 'A'): '^',

    ('^', 'A'): '>',
}
DIR_BLOCKS = [('<', '^'), ('<', 'A')]

def setup_keypads():
    develop_dictionary(NUM_KEYPAD, '0123456789A', NUM_BLOCKS)
    develop_dictionary(DIR_KEYPAD, '^>v<A', DIR_BLOCKS)

def develop_dictionary(keypad, keys, blocks):
    for key in keypad.keys():
        if key not in blocks:
            keypad[key] = [''.join(l) for l in list(set(permutations(keypad[key])))]
    keypad.update({(v, k): [invert_path(p) for p in paths] for (k, v), paths in keypad.items()})
    keypad.update({(k, k): [''] for k in keys})
    for k in keypad.keys():
        keypad[k] = [e + 'A' for e in keypad[k]]

def invert_path(path):
    return ''.join([OPPOSITE[move] for move in path[::-1]])

def first_keypad_strokes(code, start, keypad):
    return ''.join([keypad[(i, j)][0] for i, j in zip('A'+code, code)])

def all_keypad_strokes(code, start, keypad):
    if code:
        options = []
        for path in keypad[(start, code[0])]:
            options.extend([path + p for p in all_keypad_strokes(code[1:], code[0], keypad)])
        return options
    else:
        return ['']

@cache
def count_dir_keypad_strokes(seq, level):
    if level == 1:
        return sum([len(DIR_KEYPAD[(i, j)][0]) for i, j in zip('A'+seq, seq)])
    else:
        strokes = 0
        for i, j in zip('A'+seq, seq):
            strokes += min([count_dir_keypad_strokes(subseq, level-1) for subseq in DIR_KEYPAD[(i, j)]])
        return strokes
