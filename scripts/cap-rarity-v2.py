# -*- coding: utf-8 -*-
"""Cap palcalc Rarity (which is breeding weight) at 4 for in-game star display.

palcalc's Rarity field is NOT the in-game star rating. It's actually closer
to in-game display than I thought for most pals (default = 3 stars).
But the 5+ values are an artifact of palcalc's internal weighting, not
real game stars. In-game max is 4 stars.

So just cap anything > 4 down to 4.
"""
import json

pals = json.load(open('src/data/pals.json', encoding='utf-8'))

capped = 0
for pal in pals:
    r = pal.get('rarity', 3)
    if r > 4:
        pal['rarity'] = 4
        pal['updatedAt'] = '2026-07-28'
        capped += 1

print(f'Capped {capped} pals from 5+ to 4')

# Apply known game-accurate rarity overrides for important pals
# (in case palcalc value is off for the default = 3 cases)
KNOWN_RARITY = {
    'lamball': 1, 'cattiva': 1, 'chikipi': 1, 'lifmunk': 1,
    'jormuntide': 4, 'jetragon': 4, 'paladius': 4, 'necromus': 4,
    'anubis': 3, 'grizzbolt': 3, 'frostallion': 4, 'jormuntide-ignis': 4,
    'faleris': 3, 'mossanda': 3, 'warsect': 3, 'relaxaurus': 3,
    'blazamut': 4, 'blazamut-ryu': 4, 'necromus': 4, 'silvegis': 3,
    'bellanoir': 4, 'bellanoir-libero': 4,
}

override_count = 0
for pal in pals:
    slug = pal['id']
    if slug in KNOWN_RARITY and pal.get('rarity') != KNOWN_RARITY[slug]:
        pal['rarity'] = KNOWN_RARITY[slug]
        pal['updatedAt'] = '2026-07-28'
        override_count += 1

print(f'Applied {override_count} known-accuracy overrides')

from collections import Counter
dist = Counter(p.get('rarity', 0) for p in pals)
print('Final rarity distribution (capped 1-4):')
for r in sorted(dist):
    print(f'  ★{r}: {dist[r]}')

json.dump(pals, open('src/data/pals.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('Saved')
