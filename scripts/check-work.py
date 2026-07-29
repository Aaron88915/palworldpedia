# -*- coding: utf-8 -*-
"""Check which pals have generating_electricity and medicine_production work types."""
import json
from collections import Counter

pals = json.load(open('src/data/pals.json', encoding='utf-8'))

for work_type in ['generating_electricity', 'medicine_production']:
    print(f'\n=== {work_type} ===')
    matches = []
    for p in pals:
        ws = p.get('workSuitability', {})
        if work_type in ws and ws[work_type] > 0:
            matches.append((p['name']['en'], p['name']['zh'], ws[work_type]))
    print(f'Count: {len(matches)}')
    for en, zh, lvl in matches[:15]:
        print(f'  {en:30s} ({zh}) Lv {lvl}')

# Check all work types in our data
print('\n=== All work types found ===')
all_ws = Counter()
for p in pals:
    for w in p.get('workSuitability', {}).keys():
        all_ws[w] += 1
for w, cnt in all_ws.most_common():
    print(f'  {w}: {cnt} pals')
