#!/bin/env python3
import csv
import sys
from collections import defaultdict
from itertools import combinations


elos = defaultdict(lambda:1000)
k_factor = 10

reader = csv.reader(sys.stdin)

results_per_date = defaultdict(lambda:[])
for [person, date, score] in reader:
    results_per_date[date].append((person, score))


for _, results in results_per_date.items():
    for ((a, score_a), (b, score_b)) in combinations(results, 2):
        expected = 1 / (1 + pow(10, (elos[b] - elos[a]) / 400))
        error = (1 if score_a > score_b else 0) - expected
        increment = k_factor * error
        elos[a] += increment
        elos[b] -= increment

result = list(elos.items())
result.sort(key = lambda x:-x[1])
for player, rating in result:
    print(f'{player}\t{rating:.0f}')
