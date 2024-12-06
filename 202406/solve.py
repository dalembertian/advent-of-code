#!/usr/bin/env python
# encoding: utf-8

import argparse

# x, y, next
MOVEMENTS = {
    '^': (-1,  0, '>'),
    '>': ( 0,  1, 'v'),
    'v': ( 1,  0, '<'),
    '<': ( 0, -1, '^'),
}

def main(args):
    original_maze = read_lines(args.filename)

    # Part 1
    maze = [row[:] for row in original_maze]
    x, y = find_element('^', maze)[0]
    loop = walk_guard(maze)
    path = find_element('X', maze)
    print(f"Part 1 - Guard's route lenght is: {len(path)}, and he {'IS' if loop else 'is NOT'} in loop.")

    # Part 2
    # Consider all spots where guard has been, except initial and next-to-initial position
    path.remove((x,y))
    path.remove((x-1, y))
    loops = try_more_obstacles(path, original_maze)
    print(f"Part 2 - Tried {len(path)} positions for obstacles, and guard gets in loop in {loops} of them")

def read_lines(filename):
    maze = []
    with open(filename) as lines:
        for line in lines:
            maze.append(['O'] + [p for p in line.strip()] + ['O'])
    border = ['O' for i in range(len(maze[0]))]
    maze.insert(0, border)
    maze.append(border[:])
    return maze

def find_element(symbol, maze):
    found = []
    for i, row in enumerate(maze):
        for j, col in enumerate(row):
            if col == symbol:
                found.append((i,j))
    return found

def walk_guard(maze):
    direction = '^'
    x, y = find_element(direction, maze)[0]
    visited = {}
    maxx, maxy = len(maze[0])-1, len(maze)-1
    while 0 < x < maxx and 0 < y < maxy and direction not in visited.setdefault((x,y), []):
        visited[(x,y)].append(direction)
        x, y, direction = step_guard((x,y), maze)
    return direction in visited.get((x,y), [])

def step_guard(pos, maze):
    x, y = pos
    direction = maze[x][y]
    deltax, deltay, turn = MOVEMENTS[direction]
    while maze[x+deltax][y+deltay] == '#':
        direction = turn
        deltax, deltay, turn = MOVEMENTS[turn]
    maze[x][y] = 'X'
    maze[x+deltax][y+deltay] = direction
    return x+deltax, y+deltay, direction

    print(f"Part 2 - Tried {len(path)} positions for obstacles, and guard gets in loop in {loops} of them")

def try_more_obstacles(path, original_maze):
    loops = 0
    for x, y in path:
        maze = [row[:] for row in original_maze]
        maze[x][y] = '#'
        loops += 1 if walk_guard(maze) else 0
    return loops

def print_maze(maze):
    for i, line in enumerate(maze):
        print(f'{i:03} {''.join(line)}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
