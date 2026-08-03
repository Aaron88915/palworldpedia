# -*- coding: utf-8 -*-
"""Check which pals actually have biomes now."""
import json
d = json.load(open('src/data/pals.json', encoding='utf-8'))
for p in d:
    if p['id'] in ('pengullet-lux', 'flopie', 'finsider', 'finsider-ignis', 'xenovader', 'xenogard', 'bellanoir', 'bellanoir-libero', 'xenolord', 'hartalis'):
        print('%-25s -> %s' % (p['id'], p.get('biomes', [])))
