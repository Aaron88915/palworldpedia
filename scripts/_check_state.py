# -*- coding: utf-8 -*-
"""Check current state of pals.json to see if it was modified."""
import json
d = json.load(open('src/data/pals.json', encoding='utf-8'))
b = json.load(open('src/data/pals.json.bak', encoding='utf-8'))
print('Current with_biomes:', sum(1 for p in d if p.get('biomes')))
print('Backup    with_biomes:', sum(1 for p in b if p.get('biomes')))
# Find differences
for i, (a, c) in enumerate(zip(b, d)):
    if a.get('biomes') != c.get('biomes'):
        print('DIFF %s: %s -> %s' % (a['id'], a.get('biomes'), c.get('biomes')))
print('Done')
