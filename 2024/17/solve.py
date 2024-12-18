#!/usr/bin/env python
# encoding: utf-8

from argparse import ArgumentParser
from collections import defaultdict
from functools import reduce
from re import compile

def adv(ip, operand, registers, output):
    # A = A // 2**COMBO(operand)
    registers[0] = registers[0] // 2 ** COMBO[operand](registers)
    return ip + 2

def bxl(ip, operand, registers, output):
    registers[1] ^= operand
    return ip + 2

def bst(ip, operand, registers, output):
    registers[1] = COMBO[operand](registers) % 8
    return ip + 2

def jnz(ip, operand, registers, output):
    if registers[0] == 0:
        return ip + 2
    return operand

def bxc(ip, operand, registers, output):
    registers[1] = registers[1] ^ registers[2]
    return ip + 2

def out(ip, operand, registers, output):
    output.append(COMBO[operand](registers) % 8)
    return ip + 2

def bdv(ip, operand, registers, output):
    registers[1] = registers[0] // 2 ** COMBO[operand](registers)
    return ip + 2

def cdv(ip, operand, registers, output):
    registers[2] = registers[0] // 2 ** COMBO[operand](registers)
    return ip + 2

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

def run(program, registers):
    ip = 0
    output = []
    while ip < len(program):
        opcode, operand = program[ip], program[ip+1]
        ip = MACHINE[opcode](ip, operand, registers, output)
        # debug(ip, program, registers, output)
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
