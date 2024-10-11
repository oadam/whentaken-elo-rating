#!/bin/env python3
import re
import csv
import sys
from collections import defaultdict

'''
olivier
   15:22
hyper difficile
#WhenTaken #212 (26.09.2024)
I scored 724/1000 :tada:
'''

pattern = re.compile(r"(\w+.*)\n[^\n]*\n([^\n]+\n){0,2}[^\n]*#WhenTaken.*\((\d{2}\.\d{2}\.\d{4})\)\nI scored (\d+)/1000", re.MULTILINE)

lines = sys.stdin.read()
matches = pattern.findall(lines)

rows_per_person = defaultdict(lambda:0)
for (person, _, date, score) in matches:
    rows_per_person[person]+=1

writer = csv.writer(sys.stdout)
for (person, _, date, score) in matches:
    if rows_per_person[person] > 2:
        writer.writerow([person, date, int(score)])

