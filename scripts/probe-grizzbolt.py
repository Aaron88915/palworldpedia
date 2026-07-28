# -*- coding: utf-8 -*-
import json
pals = json.load(open('public/pals-data.json', encoding='utf-8'))
edges = json.load(open('public/breeding-data.json', encoding='utf-8'))
id_to_idx = {p['id']: i for i, p in enumerate(pals)}

for name in ['grizzbolt', 'orserk', 'anubis', 'shadowbeak', 'jormuntide']:
    idx = id_to_idx[name]
    producers = [e for e in edges if e[2] == idx]
    print(f'\n=== Recipes for {name} ({len(producers)} total) ===')
    # Show first 8
    for e in producers[:8]:
        a, b, c = e
        print(f'  {pals[a]["id"]} + {pals[b]["id"]} -> {pals[c]["id"]}')

# Check if any recipe uses common starters
print('\n=== Recipes for Anubis using common starters ===')
common = ['lamball', 'cattiva', 'lifmunk', 'foxparks']
common_idxs = set(id_to_idx[c] for c in common)
anubis_idx = id_to_idx['anubis']
for e in edges:
    if e[2] == anubis_idx:
        a, b, c = e
        if a in common_idxs or b in common_idxs:
            print(f'  {pals[a]["id"]} + {pals[b]["id"]} -> {pals[c]["id"]}')
