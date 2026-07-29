# -*- coding: utf-8 -*-
"""Merge palworld.gg work data into pals.json, adding missing entries."""
import json
from collections import Counter

pals = json.load(open('src/data/pals.json', encoding='utf-8'))
gg_works = json.load(open('scripts/gg-work-by-name.json', encoding='utf-8'))

# Build our pals by en name
our_by_en = {p['name']['en'].lower().strip(): p for p in pals}

# Stats
added = 0
updated = 0
not_found = []
work_dist = Counter()
for en_name, work in gg_works.items():
    en_lower = en_name.lower().strip()
    pal = our_by_en.get(en_lower)
    if not pal:
        not_found.append(en_name)
        continue
    ws = pal.setdefault('workSuitability', {})
    for k, v in work.items():
        if v > 0:
            old = ws.get(k, 0)
            if old == 0:
                added += 1
            elif old != v:
                updated += 1
            ws[k] = v
            work_dist[k] += 1

print(f'Added: {added}, Updated: {updated}')
print(f'\nWork distribution now:')
for w, cnt in Counter(p.get('workSuitability', {}).get(k, 0) > 0 for p in pals for k in p.get('workSuitability', {})).most_common():
    pass
# Better distribution
all_ws = Counter()
for p in pals:
    for w in p.get('workSuitability', {}):
        all_ws[w] += 1
for w, cnt in all_ws.most_common():
    print(f'  {w}: {cnt}')

print(f'\nNot found in our DB ({len(not_found)}):')
for n in not_found[:20]:
    print(f'  {n}')

# Show electricity/medicine specifically
print('\n=== Electricity ===')
for p in pals:
    if p.get('workSuitability', {}).get('generating_electricity', 0) > 0:
        print(f'  {p["name"]["en"]:30s} ({p["name"]["zh"]}) Lv {p["workSuitability"]["generating_electricity"]}')

print('\n=== Medicine ===')
for p in pals:
    if p.get('workSuitability', {}).get('medicine_production', 0) > 0:
        print(f'  {p["name"]["en"]:30s} ({p["name"]["zh"]}) Lv {p["workSuitability"]["medicine_production"]}')

json.dump(pals, open('src/data/pals.json', 'w', encoding='utf-8'),
          ensure_ascii=False, indent=0)
print('\nSaved pals.json')
