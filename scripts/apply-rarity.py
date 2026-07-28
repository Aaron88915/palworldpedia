# -*- coding: utf-8 -*-
"""Apply paldb.cc rarity to pals.json - replace existing broken rarity, add rarityTier."""
import json
from collections import Counter

pals = json.load(open('src/data/pals.json', encoding='utf-8'))
rarity_data = json.load(open('scripts/paldb-rarity.json', encoding='utf-8'))

def to_tier(r):
    if r >= 20: return 'Legendary'
    if r >= 8: return 'Epic'
    if r >= 5: return 'Rare'
    return 'Common'

updated = 0
missing = []
for pal in pals:
    palid = pal['id']
    if palid not in rarity_data:
        missing.append(palid)
        continue
    r = rarity_data[palid]
    pal['rarity'] = r
    pal['rarityTier'] = to_tier(r)
    updated += 1

print(f'Updated: {updated}')
print(f'Missing: {len(missing)}')
if missing:
    print(f'  {missing}')

# Distribution
tier_cnt = Counter(p['rarityTier'] for p in pals if 'rarityTier' in p)
print(f'\n--- Final distribution ---')
for tier in ['Common', 'Rare', 'Epic', 'Legendary']:
    print(f'  {tier}: {tier_cnt.get(tier, 0)}')

# Save
json.dump(pals, open('src/data/pals.json', 'w', encoding='utf-8'),
          ensure_ascii=False, indent=0)
print(f'\nSaved pals.json')

# Verify 7 known legendaries are at 20
print('\n--- Legendary verification (should all be R20) ---')
for pal in pals:
    if pal.get('rarityTier') == 'Legendary':
        print(f'  {pal["name"]["en"]:30s} R{pal["rarity"]} ({pal["name"]["zh"]})')
