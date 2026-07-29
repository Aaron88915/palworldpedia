# -*- coding: utf-8 -*-
import json
pals = json.load(open('src/data/pals.json', encoding='utf-8'))
with_biomes = [p for p in pals if p.get('biomes')]
print(f'Pals with biomes: {len(with_biomes)}')
for p in with_biomes[:5]:
    print(f"  {p['id']:30s} -> {p['biomes']}")
print()
# Check fetch-pals.mjs to see where biomes came from
