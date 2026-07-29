# -*- coding: utf-8 -*-
"""
Revert wrong rarity fix and apply correct cap.

Original data had: most pals = 3, some 5-10 for special variants.
The user is right: in-game max is 4 stars.

The cleanest fix: cap rarity at 4, but DON'T remap most pals down to 1.
Most common/rare pals in palcalc are Rarity=3, which actually IS the
default visual rarity in Palworld 1.0 (most pals = 3 stars).

So just cap anything > 4 down to 4.
"""
import json

pals = json.load(open('src/data/pals.json', encoding='utf-8'))

updated = 0
for pal in pals:
    r = pal.get('rarity', 3)
    if r > 4:
        pal['rarity'] = 4
        pal['updatedAt'] = '2026-07-28'
        updated += 1

print(f'Capped {updated} pals from 5+ to 4')

from collections import Counter
dist = Counter(p.get('rarity', 0) for p in pals)
print('Final rarity distribution:')
for r in sorted(dist):
    print(f'  ★{r}: {dist[r]}')

json.dump(pals, open('src/data/pals.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('Saved')
