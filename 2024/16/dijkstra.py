#!/usr/bin/env python
# encoding: utf-8

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
INFINITE = float('inf')

def find_shortest_path(start, nodes):
    # Travels graph finding smallest cost from start
    # Returns False if not all nodes are connected

    # Mark all unvisited nodes with distance "infinite" from start - except start
    unvisited = list(nodes.keys())
    for node in unvisited:
        nodes[node]['cost'] = INFINITE
    nodes[start]['cost'] = 0

    while unvisited:
        # Get unvisited node with shortest distance to start
        unvisited.sort(key=lambda n: nodes[n]['cost'])
        this = unvisited.pop(0)
        if nodes[this]['cost'] == INFINITE:
            break

        # Visits every node linked to this STILL IN unvisited
        for v, (cost, path) in nodes[this]['nodes'].items():
            if v in unvisited:
                new_cost = nodes[this]['cost'] + cost
                if new_cost < nodes[v]['cost']:
                    # print(f'{this} -> {v} ({new_cost})')
                    # input()
                    nodes[v]['cost'] = new_cost
                    nodes[v].setdefault('prev_path', []).append(invert_path(path))
                    nodes[v].setdefault('prev_node', []).append(this)
    return False if unvisited else True

def trace_back(start, finish, nodes):
    # Builds path from finish to start, if existing
    path = ''
    cost = INFINITE
    node = finish
    if nodes[finish]:
        while node != start:
            path += nodes[node]['prev_path'][0]
            node  = nodes[node]['prev_node'][0]
        cost = nodes[finish]['cost']
    return invert_path(path), cost

def invert_path(path):
    return ''.join([OPPOSITE[move] for move in path[::-1]])

def print_nodes(nodes):
    for k in nodes.keys():
        print(f'{k}: {nodes[k]}')
    print()
