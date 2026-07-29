# -*- coding: utf-8 -*-
"""Fix work suitability keys in pals.json to match UI config."""
import json
from collections import Counter

pals = json.load(open('src/data/pals.json', encoding='utf-8'))

# Map: old name -> new name (matching UI config.ts)
KEY_MAP = {
    'electricity': 'generating_electricity',
    'medicine': 'medicine_production',
}

fixed = 0
new_dist = Counter()
for p in pals:
    ws = p.get('workSuitability', {})
    for old, new in KEY_MAP.items():
        if old in ws:
            ws[new] = ws.pop(old)
            fixed += 1
    for w in ws.keys():
        new_dist[w] += 1

print(f'Fixed {fixed} work keys')
print(f'\nNew distribution:')
for w, cnt in new_dist.most_common():
    print(f'  {w}: {cnt}')

# Show pals with electricity/medicine
print('\n=== generating_electricity pals ===')
for p in pals:
    if 'generating_electricity' in p.get('workSuitability', {}):
        print(f'  {p["name"]["en"]:30s} ({p["name"]["zh"]}) Lv {p["workSuitability"]["generating_electricity"]}')

print('\n=== medicine_production pals ===')
for p in pals:
    if 'medicine_production' in p.get('workSuitability', {}):
        print(f'  {p["name"]["en"]:30s} ({p["name"]["zh"]}) Lv {p["workSuitability"]["medicine_production"]}')

json.dump(pals, open('src/data/pals.json', 'w', encoding='utf-8'),
          ensure_ascii=False, indent=0)
print('\nSaved pals.json')
