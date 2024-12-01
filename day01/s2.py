#!/usr/bin/env python
# encoding: utf-8

import csv
import collections

a = []
b = []

with open("input.txt") as csvfile:
    reader = csv.reader(csvfile, delimiter=' ', quotechar='\"')
    for line in reader:
        a.append(int(line[0]))
        b.append(int(line[3]))
print('%d lines' % len(a))

a.sort()
b.sort()

distance = 0
for i in range(len(a)):
    diff = abs(a[i] - b[i])
    distance += diff
    # print('%d\t%d\t%d\t%d' % (a[i], b[i], diff, distance))

print('Distance is %d\n' % distance)

a_count = collections.Counter(a)
b_count = collections.Counter(b)

print('Duplicates: %d %d' % (
    sum([count for item, count in a_count.items() if count > 1]),
    sum([count for item, count in b_count.items() if count > 1])
))

similarity = 0
for key in a:
    score = b_count.get(key, 0)
    similarity += key * score
    # print('%d\t%d\t%d' % (key, score, similarity))

print('Similarity is %d\n' % similarity)
