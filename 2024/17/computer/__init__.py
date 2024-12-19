#!/usr/bin/env python
# encoding: utf-8

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
