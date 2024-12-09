#!/usr/bin/env python
# encoding: utf-8

import argparse

def main(args):
    line = read_lines(args.filename)

    filesystem = expand_filesystem(line)
    compact_filesystem(filesystem)
    print(f'Part 1 - Checksum of filesystem is: {checksum(filesystem)}')

    block, size, space = index(line)
    find_full_space(block, size, space)
    filesystem = interpolate_blocks_and_spaces(block, size, space)
    print(f'Part 2 - Checksum of filesystem is: {checksum(filesystem)}')

def index(line):
    # Split the entry in 3 separate data structures
    block = []
    size  = {}
    space = []
    for i in range(len(line) // 2):
        block.append(i)
        size[i] = int(line[i*2])
        space.append(int(line[i*2 + 1]))
    return block, size, space

def find_full_space(block, size, space):
    for i in range(len(block)-1, 1, -1):
        # Tricky: which spaces to check? *All* to the left!
        pos = block.index(i)
        for j in range(pos):
            if size[i] <= space[j]:
                block.pop(pos)
                block.insert(j+1, i)
                space[j] -= size[i]
                space[pos] += space[pos-1] + size[i]
                space.pop(pos-1)
                space.insert(j, 0)
                break

def interpolate_blocks_and_spaces(block, size, space):
    filesystem = []
    for i in range(len(block)):
        ID = block[i]
        filesystem.extend([ID for j in range(size[ID])])
        filesystem.extend([0 for j in range(space[i])])
    return filesystem    

def expand_filesystem(line):
    filesystem = []
    for i in range(len(line) // 2):
        filesystem.extend([i for j in range(int(line[i*2]))])
        filesystem.extend([-1 for j in range(int(line[i*2 + 1]))])
    return filesystem

def compact_filesystem(filesystem):
    try:
        while True:
            pos = filesystem.index(-1)
            filesystem[pos] = filesystem.pop()
    except:
        pass

def checksum(filesystem):
    return sum(i * j for i, j in enumerate(filesystem))

def read_lines(filename):
    with open(filename) as lines:
        return lines.readline().strip() + '0'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
