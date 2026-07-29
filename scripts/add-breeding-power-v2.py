# -*- coding: utf-8 -*-
"""Add breeding power using palcalc Name field (English display name) for matching."""
import json

pals = json.load(open('src/data/pals.json', encoding='utf-8'))
db = json.load(open('scripts/raw-palcalc-db.json', encoding='utf-8'))

# Build name (English) -> breeding power map
bp_by_name = {p['Name']: p.get('BreedingPower', 0) for p in db['Pals']}

# Map breeding power to rank
def bp_to_rank(bp):
    if bp <= 0: return 0
    if bp < 500: return 1
    if bp < 1000: return 2
    if bp < 1500: return 3
    if bp < 2500: return 4
    return 5

updated = 0
no_data = []
for pal in pals:
    en_name = pal.get('name', {}).get('en', '')
    bp = bp_by_name.get(en_name, 0)
    if bp == 0:
        no_data.append((pal['id'], en_name))
        continue
    pal['breedRank'] = bp_to_rank(bp)
    pal['breedPower'] = bp
    pal['updatedAt'] = '2026-07-28'
    updated += 1

print(f'Added breeding rank to {updated} pals')
print(f'No data for {len(no_data)} pals')
for n in no_data[:10]:
    print(f'  {n}')

from collections import Counter
dist = Counter(p.get('breedRank', 0) for p in pals)
print('Breed rank distribution:')
for r in sorted(dist):
    print(f'  ★{r}: {dist[r]}')

json.dump(pals, open('src/data/pals.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('Saved')
