#!/usr/bin/env python
# encoding: utf-8


INFINITE = float('inf')


def find_shortest_path(nodes, start):
    # CAREFUL: simplified Dijkstra for connections with cost zero
    # (see 2024/16 or 2024/18 for a real Dijkstra implementation)
    # Returns False if not all nodes are connected

    # Mark all unvisited nodes with distance "infinite" from start - except start
    unvisited = list(nodes.keys())
    for node in unvisited:
        nodes[node]['cost']  = INFINITE
        nodes[node]['paths'] = []
        nodes[node]['previous'] = []
    nodes[start]['cost'] = 0
    nodes[start]['paths'].append([])

    while unvisited:
        # Get unvisited node with shortest distance to start
        unvisited.sort(key=lambda n: nodes[n]['cost'])
        this = unvisited.pop(0)
        if nodes[this]['cost'] == INFINITE:
            break

        # Visits every node linked to this STILL IN unvisited
        for v in nodes[this].get('next', []):
            if v in unvisited:
                if nodes[v]['cost'] >= 0:
                    nodes[v]['cost'] = 0
                    for path in nodes[this]['paths']:
                        next_path = path[:]
                        next_path.append(this)
                        nodes[v]['paths'].append(next_path)
                    nodes[v]['previous'].append(this)
    return False if unvisited else True


def print_paths(nodes, end):
    for path in nodes[end]['paths']:
        print(path)


def print_nodes(nodes):
    for key in nodes.keys():
        print(f'{key}: {nodes[key]}')
    print()
