# -*- coding: utf-8 -*-
"""Verify that existing pals weren't changed."""
import json
d = json.load(open('src/data/pals.json', encoding='utf-8'))
b = json.load(open('src/data/pals.json.bak', encoding='utf-8'))

# Find changed pals
diff_count = 0
for a, c in zip(b, d):
    if a.get('biomes') != c.get('biomes'):
        diff_count += 1
        if a.get('biomes'):
            # Had biomes, was changed
            print('CHANGED: %s' % a['id'])
            print('  before: %s' % a.get('biomes'))
            print('  after:  %s' % c.get('biomes'))
        else:
            # Was empty, now filled
            print('FILLED:  %s -> %s' % (a['id'], c.get('biomes')))

print()
print('Total changes: %d' % diff_count)
print('Pals with biomes now: %d / %d' % (sum(1 for p in d if p.get('biomes')), len(d)))
print('Pals with biomes before: %d / %d' % (sum(1 for p in b if p.get('biomes')), len(b)))
