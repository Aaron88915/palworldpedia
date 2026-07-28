# -*- coding: utf-8 -*-
"""Audit current rarity distribution - fixed keys."""
import json
from collections import Counter

with open('src/data/pals.json', 'r', encoding='utf-8') as f:
    pals = json.load(f)

print(f'Total pals: {len(pals)}')
print()

# Rarity distribution
rarity_counter = Counter()
for p in pals:
    r = p.get('rarity', None)
    rarity_counter[r] += 1

print('--- Current rarity distribution (1-4 scale) ---')
for r in sorted([k for k in rarity_counter.keys() if k is not None]):
    print(f'  Rarity {r}: {rarity_counter[r]}')
print(f'  None/missing: {rarity_counter.get(None, 0)}')
print()

# 7 official Legendaries from Grok
legend_names = ['Jetragon', 'Frostallion', 'Frostallion Noct', 'Paladius', 'Necromus', 'Neptilius', 'Panthalus']
print('--- 7 official Legendaries check ---')
for p in pals:
    en = p.get('name', {}).get('en', '')
    if en in legend_names:
        bp = p.get('breedPower') or p.get('breedpower') or 0
        print(f'  [OK] {en} ({p["name"]["zh"]}) - rarity={p.get("rarity")}, breedPower={bp}, breedRank={p.get("breedRank")}')

print('\n--- All pals with rarity=4 (current Legendary tier) ---')
r4 = [p for p in pals if p.get('rarity') == 4]
print(f'Count: {len(r4)}')
for p in r4:
    en = p.get('name', {}).get('en', '?')
    zh = p.get('name', {}).get('zh', '?')
    bp = p.get('breedPower') or p.get('breedpower') or 0
    print(f'  {en} ({zh}) - BP={bp}')

# Check if Panthalus exists
print('\n--- 1.0 new legendaries from Grok (Panthalus) ---')
for p in pals:
    en = p.get('name', {}).get('en', '')
    if 'Panthal' in en or '潘' in p.get('name', {}).get('zh', ''):
        print(f'  {en} ({p["name"]["zh"]}) - rarity={p.get("rarity")}')

# Distribution comparison
print('\n--- vs Grok expected ---')
print(f'  Common (1?):   expect 120-140  actual R1+R2+R3 = ?')
print(f'  Rare (2?):     expect 80-100')
print(f'  Epic (3?):     expect 40-60')
print(f'  Legendary (4): expect 8-15  actual R4 = {rarity_counter.get(4, 0)}')

# The 4-tier is too coarse for 288 pals. Let's see if a finer scale fits.
# Grok says 287 official. So we should have something like 130/90/55/12 if it matches 4-tier.
# If current R4=15, that's close to "Legendary 8-15". But R3=260 is way more than Epic 40-60.
# This means our current scale is NOT Common/Rare/Epic/Legendary. It might be something else.

# Let's see if we can compute from breedPower
# Lamball BP=3050 = Rank 1
# Frostallion BP should be very low (legendary, hard to breed)
print('\n--- breedPower range check ---')
bps = [p.get('breedPower') or p.get('breedpower') or 0 for p in pals]
print(f'  min={min(bps)}, max={max(bps)}, avg={sum(bps)/len(bps):.0f}')
buckets = Counter()
for bp in bps:
    if bp == 0:
        buckets['0'] += 1
    elif bp < 500:
        buckets['<500'] += 1
    elif bp < 1000:
        buckets['500-1k'] += 1
    elif bp < 1500:
        buckets['1k-1.5k'] += 1
    elif bp < 2000:
        buckets['1.5k-2k'] += 1
    elif bp < 2500:
        buckets['2k-2.5k'] += 1
    else:
        buckets['2.5k+'] += 1
for k in ['0', '<500', '500-1k', '1k-1.5k', '1.5k-2k', '2k-2.5k', '2.5k+']:
    print(f'  {k}: {buckets[k]}')
