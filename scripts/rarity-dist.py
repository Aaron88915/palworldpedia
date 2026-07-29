# -*- coding: utf-8 -*-
import json
pals = json.load(open('src/data/pals.json', encoding='utf-8'))
from collections import Counter
rarity_dist = Counter(p.get('rarity', 0) for p in pals)
print('Rarity distribution:')
for r in sorted(rarity_dist):
    print(f'  ★{r}: {rarity_dist[r]}')

# Top rarity 4+ pals
r4plus = [p for p in pals if p.get('rarity', 0) >= 4]
print(f'\nRarity 4+: {len(r4plus)}')
for p in r4plus[:15]:
    n = p['name']['zh']
    print(f'  ★{p["rarity"]} {p["id"]:25s} - {n}')
