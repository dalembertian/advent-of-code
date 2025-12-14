#!/usr/bin/env python
# encoding: utf-8


from collections import deque


INFINITE = float('inf')


def count_paths(nodes, passing_by):
    first, second = passing_by
    runs = [['svr', first, second, 'out'], ['svr', second, first, 'out']]
    total = 0
    for run in runs:
        subtotal = 1
        for i in range(3):
            find_shortest_path(nodes, run[i])
            subtotal *= nodes[run[i+1]].get('count', 0)
        total += subtotal
    return total


def find_shortest_path(nodes, start, record_paths = False):
    # Simplified Dijkstra for connections with cost zero
    # (see 2024/16 or 2024/18 for a real Dijkstra implementation)
    # Returns False if not all nodes are connected

    # Mark all unvisited nodes with distance "infinite" from start - except start
    unvisited = list(nodes.keys())
    for node in unvisited:
        nodes[node]['cost']  = INFINITE
        nodes[node]['count'] = 0
        nodes[node]['paths'] = []
        nodes[node]['previous'] = []
    nodes[start]['cost'] = 0
    nodes[start]['count'] = 1
    nodes[start].get('paths', []).append([])

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
                    nodes[v]['count'] += nodes[this]['count']
                    nodes[v]['previous'].append(this)
                    if record_paths:
                        for path in nodes[this]['paths']:
                            next_path = path[:]
                            next_path.append(this)
                            nodes[v]['paths'].append(next_path)
    return False if unvisited else True


def check_paths(nodes, end, required):
    visited = []
    current = required[:]
    if check_current_path(nodes, end, visited, current):
        return True
    return False


def check_current_path(nodes, end, visited, current):
    # If already visited in this current check, it's cyclic
    if end in current:
        current.remove(end)
    if not current:
        return True

    # If already visited previously, no need to check it again
    if end in visited:
        return False

    current.append(start)
    visited.append(start)
    links = nodes[start].get('next', [])
    if any([is_current_cyclic(nodes, link, visited, current) for link in links]):
        return True

    # Remove from current check before returning
    current.remove(start)
    return False


def print_paths(nodes, end):
    for path in nodes[end]['paths']:
        print(path)


def print_nodes(nodes):
    for key in nodes.keys():
        print(f'{key}: {nodes[key]}')
    print()


def is_cyclic(nodes, start):
    # DFS check looking for cycles
    visited = []
    current = []
    if is_current_cyclic(nodes, start, visited, current):
        return True
    return False


def is_current_cyclic(nodes, start, visited, current):
    # If already visited in this current check, it's cyclic
    if start in current:
        return True

    # If already visited previously, no need to check it again
    if start in visited:
        return False

    current.append(start)
    visited.append(start)
    links = nodes[start].get('next', [])
    if any([is_current_cyclic(nodes, link, visited, current) for link in links]):
        return True

    # Remove from current check before returning
    current.remove(start)
    return False
