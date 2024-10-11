#!/bin/env python3
import re
import csv
import sys
from collections import defaultdict

'''
olivier
   15:22
hyper difficile
15:22
#WhenTaken #212 (26.09.2024)
I scored 724/1000 :tada:
'''

writer = csv.writer(sys.stdout)

lines = sys.stdin.read().split('\n')
person_pattern = re.compile(r"^[a-z]+$")
date_pattern = re.compile(r"#WhenTaken.*\((\d{2}\.\d{2}\.\d{4})\)")
score_pattern = re.compile(r"I scored (\d+)/1000")
for i in range(1, len(lines) - 1):
    date_match = date_pattern.match(lines[i])
    if not date_match:
        continue
    score_match = score_pattern.match(lines[i+1])
    if not score_match:
        print(f'could not match : {lines[i+1]}')
        continue
    j = i - 1
    while j >= 0 and j > i - 6:
        if person_pattern.match(lines[j]):
            person = lines[j]
            break
        j -= 1
    else:
        print(f'could not match personne for : {score_match[0]}')
        continue
    writer.writerow([person, date_match[1], score_match[1]])

