#!/usr/bin/env python
# encoding: utf-8

import argparse
import re


def main(args):
    secrets = read_lines(args.filename)
    amount  = int(args.number)
    
    total, seqs, difs = generate(secrets, amount)
    print(f'Part 1 - Sum of all {amount} secrets: {total}')

    bananas = assess_offers(seqs, difs, amount)
    print(f'Part 2 - Most amount of bananas: {bananas[-1]}')

def assess_offers(seqs, difs, amount):
    # Assess all (amount-1) offers per buyer, tabulating the first one
    offers = {}
    buyers = len(seqs)
    for i in range(1, amount-2):
        for j, (seq, dif) in enumerate(zip(seqs, difs)):
            key = tuple(dif[i:i+4])
            val = offers.setdefault(key, [''] * buyers)
            if val[j] == '':
                val[j] = seq[i+3]
    return sorted([sum([i for i in v if i != '']) for v in offers.values()])

def generate(secrets, amount):
    # For each buyer, calculates secrets #amount times, and
    # returns seq with last-digits, and differences
    seqs = []
    difs = []
    total = 0
    for secret in secrets:
        seq = [secret % 10]
        dif = [0]
        n = secret
        for i in range(amount):
            n = next_secret(n)
            seq.append(n % 10)
            dif.append(seq[i+1] - seq[i])
        total += n
        seqs.append(seq)
        difs.append(dif)
    return total, seqs, difs

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
    parser.add_argument("--number", "-n", default="2000", help="Number of secrets to generate (def: 2000)")
    args = parser.parse_args()
    main(args)
