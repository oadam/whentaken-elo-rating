#!/bin/env python3
import csv
import sys
from datetime import datetime
from collections import defaultdict
from itertools import combinations


elos = defaultdict(lambda:1000)
k_factor = 20

reader = csv.reader(sys.stdin)
writer = csv.writer(sys.stdout)

all_persons = set()
results_per_date = defaultdict(lambda:[])
for person, date_string, score in set((x[0], x[1], x[2]) for x in reader):
    results_per_date[datetime.strptime(date_string, "%d.%m.%Y")].append((person, score))
    all_persons.add(person)

all_persons = list(all_persons)
all_persons.sort()

writer.writerow(['date'] + all_persons)

sorted_result = list(results_per_date.items())
sorted_result.sort(key=lambda x:x[0])

for d, results in sorted_result:
    for ((a, score_a), (b, score_b)) in combinations(results, 2):
        expected = 1 / (1 + pow(10, (elos[b] - elos[a]) / 400))
        error = (1 if score_a > score_b else 0) - expected
        increment = k_factor * error
        elos[a] += increment
        elos[b] -= increment
    writer.writerow([d.strftime("%d/%m/%Y")] + [int(elos[p]) for p in all_persons])
