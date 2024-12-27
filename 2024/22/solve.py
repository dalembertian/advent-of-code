#!/usr/bin/env python
# encoding: utf-8

import argparse
import re

def main(args):
    secrets = read_lines(args.filename)
    
    total = 0
    for secret in secrets:
        n = secret
        for i in range(2000):
            n = next_secret(n)
        total += n
        # print(f'{secret}: {n}')
    print(f'Part 1 - Sum of all 2000th Secrets: {total}')

def next_secret(secret):
    secret = prune(mix(secret, secret * 64))
    secret = prune(mix(secret, secret // 32))
    secret = prune(mix(secret, secret * 2048))
    return secret

def mix(secret, number):
    secret = secret ^ number
    return secret

def prune(secret):
    secret = secret % 16777216 # 2 exp 24
    return secret

def read_lines(filename):
    with open(filename) as input:
        return [int(line.strip()) for line in input.readlines()]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help='Input file to process')
    args = parser.parse_args()
    main(args)
