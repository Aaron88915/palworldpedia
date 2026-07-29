# -*- coding: utf-8 -*-
"""
Fix rarity data.

palcalc's `Rarity` field is a breeding weight, not in-game star rating.
In Palworld 1.0, the visual rarity is 1-4 stars:
  1 star = Common
  2 stars = Uncommon
  3 stars = Rare
  4 stars = Epic (including most boss/alpha)

We remap:
  palcalc Rarity 1-3  -> game 1
  palcalc Rarity 4-5  -> game 2
  palcalc Rarity 6-7  -> game 3
  palcalc Rarity 8-10 -> game 4

Special cases (legendary/boss): 4
"""
import json

pals = json.load(open('src/data/pals.json', encoding='utf-8'))
db = json.load(open('scripts/raw-palcalc-db.json', encoding='utf-8'))

# Build palcalc rarity lookup by InternalName
palcalc_rarity = {p['InternalName']: p.get('Rarity', 0) for p in db['Pals']}

def slug_to_internal(slug):
    return '_'.join(p.capitalize() for p in slug.split('-'))

def remap_rarity(palcalc_r):
    if palcalc_r <= 3: return 1
    if palcalc_r <= 5: return 2
    if palcalc_r <= 7: return 3
    return 4

updated = 0
for pal in pals:
    iname = slug_to_internal(pal['id'])
    pcr = palcalc_rarity.get(iname, 0)
    new_rarity = remap_rarity(pcr)
    if pal.get('rarity') != new_rarity:
        pal['rarity'] = new_rarity
        pal['updatedAt'] = '2026-07-28'
        updated += 1

print(f'Updated {updated} pals with corrected rarity')

# Verify distribution
from collections import Counter
dist = Counter(p.get('rarity', 0) for p in pals)
print('New rarity distribution:')
for r in sorted(dist):
    print(f'  ★{r}: {dist[r]}')

json.dump(pals, open('src/data/pals.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('Saved')
