# -*- coding: utf-8 -*-
"""Add breeding power (rank) to pals.json based on palcalc BreedingPower field.

palcalc's BreedingPower is a 1-1500+ integer where lower = easier to breed.
We map to a 1-5 star rank for display in the breeding calculator dropdowns.
"""
import json

pals = json.load(open('src/data/pals.json', encoding='utf-8'))
db = json.load(open('scripts/raw-palcalc-db.json', encoding='utf-8'))

# Build InternalName -> breeding power map
bp_by_iname = {p['InternalName']: p.get('BreedingPower', 0) for p in db['Pals']}

def slug_to_internal(slug):
    return '_'.join(p.capitalize() for p in slug.split('-'))

# Map breeding power to rank
# <500 = 1 star (very easy, e.g. Lamball)
# <1000 = 2 stars
# <1500 = 3 stars
# <2500 = 4 stars
# >=2500 = 5 stars (very hard, e.g. Frostallion)
def bp_to_rank(bp):
    if bp < 500: return 1
    if bp < 1000: return 2
    if bp < 1500: return 3
    if bp < 2500: return 4
    return 5

# Apply
updated = 0
no_data = []
for pal in pals:
    iname = slug_to_internal(pal['id'])
    bp = bp_by_iname.get(iname, 0)
    if bp == 0:
        no_data.append(pal['id'])
        continue
    pal['breedRank'] = bp_to_rank(bp)
    pal['breedPower'] = bp
    pal['updatedAt'] = '2026-07-28'
    updated += 1

print(f'Added breeding rank to {updated} pals')
print(f'No data for {len(no_data)} pals: {no_data[:10]}')

# Verify distribution
from collections import Counter
dist = Counter(p.get('breedRank', 0) for p in pals)
print('Breed rank distribution:')
for r in sorted(dist):
    print(f'  ★{r}: {dist[r]}')

json.dump(pals, open('src/data/pals.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('Saved')
