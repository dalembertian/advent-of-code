#!/usr/bin/env python
# encoding: utf-8

from argparse import ArgumentParser
from collections import defaultdict
from functools import reduce
from re import compile

def adv(ip, operand, registers):
    registers[0] = registers[0] // 2 ** COMBO[operand](registers)
    return ip + 2, None

def bxl(ip, operand, registers):
    registers[1] ^= operand
    return ip + 2, None

def bst(ip, operand, registers):
    registers[1] = COMBO[operand](registers) % 8
    return ip + 2, None

def jnz(ip, operand, registers):
    if registers[0] == 0:
        return ip + 2, None
    return operand, None

def bxc(ip, operand, registers):
    registers[1] = registers[1] ^ registers[2]
    return ip + 2, None

def out(ip, operand, registers):
    return ip + 2, COMBO[operand](registers) % 8

def bdv(ip, operand, registers):
    registers[1] = registers[0] // 2 ** COMBO[operand](registers)
    return ip + 2, None

def cdv(ip, operand, registers):
    registers[2] = registers[0] // 2 ** COMBO[operand](registers)
    return ip + 2, None

COMBO = {
    0: lambda reg: 0,
    1: lambda reg: 1,
    2: lambda reg: 2,
    3: lambda reg: 3,
    4: lambda reg: reg[0],
    5: lambda reg: reg[1],
    6: lambda reg: reg[2],
}
MACHINE  = {0: adv, 1: bxl, 2: bst, 3: jnz, 4: bxc, 5: out, 6: bdv, 7: cdv}
ASSEMBLY = {'adv': adv, 'bxl': bxl, 'bst': bst, 'jnz': jnz, 'bxc': bxc, 'out': out, 'bdv': bdv, 'cdv': cdv}

def main(args):
    program, registers = read_lines(args.filename)

    output = run(program, registers)
    print(f'Part 1 - Final Output: {','.join([str(o) for o in output])}')

    A = search_itself(program, registers)
    if A:
        new_registers = [A, registers[1], registers[2]]
        output = run(program, new_registers)
        print(f'Part 2 - A: {A}')
        print(f'Program: {','.join([str(o) for o in program])}')
        print(f'Output: {','.join([str(o) for o in output])}')
    else:
        print(f'Couldn\'t find A... :-(')

def search_itself(program, initial_registers):
    max_size = len(program)
    registers = initial_registers[:]
    A, B, C = registers
    A = -1
    while A < 100000000:
        A += 1
        if A % 1000000 == 0:
            print(A, '...')
        ip = 0
        target = 0
        registers[0], registers[1], registers[2] = A, B, C
        while ip < len(program):
            opcode, operand = program[ip], program[ip+1]
            ip, output = MACHINE[opcode](ip, operand, registers)
            # debug(ip, program, registers, output)
            # print(f'target: {target}')
            # input()
            if output != None:
                if target == max_size or output != program[target]:
                    target += 1
                    break
                target += 1
        if target == max_size:
            break
    if target == max_size:
        return A
    else:
        return None

def run(program, initial_registers):
    registers = initial_registers[:]
    ip = 0
    output = []
    while ip < len(program):
        opcode, operand = program[ip], program[ip+1]
        ip, out = MACHINE[opcode](ip, operand, registers)
        if out != None:
            output.append(out)
        # debug(ip, program, registers, out)
    return output

def debug(ip, program, registers, output):
    print(program)
    print(registers)
    if ip < len(program):
        print(f'ip: {ip}, opcode: {program[ip]} ({MACHINE[program[ip]]}), operand: {program[ip+1]}')
    print(f'output: {output}')
    print()

def read_lines(filename):
    values = compile(r'([\d+,?]+)')
    registers = []
    with open(filename) as input:
        for i in range(3):
            registers.append(int(values.search(input.readline()).group(0)))
        input.readline()
        program = [int(i) for i in values.search(input.readline()).group(0).split(',')]
    return program, registers

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
