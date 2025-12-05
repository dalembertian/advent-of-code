#!/usr/bin/env python
# encoding: utf-8

import argparse


class TreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


def main(args):
    freshes, ingredients = read_lines(args.filename)
    
    root = TreeNode(freshes[0])
    for fresh in freshes:
        insert_node(fresh, root)

    # Correct: 567
    print(f'Part 1 - fresh ingredients: {sum([find_element(i, root) for i in ingredients])}')


def find_element(e, node):
    if not node:
        return False
    a, b = node.data
    if e >= a and e <=b:
        return True
    if e < a:
        return find_element(e, node.left)
    else:
        return find_element(e, node.right)


def insert_node(pair, node):
    a, b = pair
    na, nb = node.data
    if a >= na and b <= nb:
        return
    if a < na:
        if node.left:
            insert_node(pair, node.left)
        else:
            node.left = TreeNode((a,b))
    if b > nb:
        if node.right:
            insert_node(pair, node.right)
        else:
            node.right = TreeNode((a,b))


def show_tree(node, level=0, prefix=''):
    if node:
        print(f'{' '*level}{prefix}', end=' ')
        print(node.data)
        show_tree(node.left, level+1, 'L')
        show_tree(node.right, level+1, 'R')


def read_lines(filename):
    freshes = []
    ingredients = []
    with open(filename) as lines:
        while line := lines.readline().strip():
            a, b = line.split('-')
            freshes.append((int(a), int(b)))
        while line := lines.readline():
            ingredients.append(int(line))
    return freshes, ingredients


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
