# -*- coding: utf-8 -*-
"""Extract breeding data structure from main JS bundle."""
import re, json, os

# Load main bundle
with open('scripts/palworldgg-bundles/Crnsudxy.js', 'r', encoding='utf-8') as f:
    data = f.read()

print(f'Bundle size: {len(data)}')

# Find big JSON arrays (likely the pal/breed data)
# Look for breeding, combination, combiRank, etc.
print('\n--- Key term occurrences ---')
for kw in ['combiRank', 'combo', 'breed', 'Breed', 'specialCombination', 'Special']:
    cnt = data.count(kw)
    print(f'  {kw}: {cnt}')

# Find data structure around combiRank
idx = data.find('combiRank')
while idx > 0:
    print(f'\n--- combiRank @ {idx} ---')
    print(data[max(0,idx-200):idx+500])
    idx = data.find('combiRank', idx + 1)
    if idx > 100000:
        break

# Find "name" property (pal names)
print('\n--- First 20 occurrences of pal names pattern ---')
m = re.search(r'name:\s*[\"\']Lamball[\"\']', data)
if m:
    print(f'  Lamball pattern @ {m.start()}')
    print(data[max(0, m.start()-300):m.start()+800])
