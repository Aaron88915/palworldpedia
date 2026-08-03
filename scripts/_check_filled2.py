# -*- coding: utf-8 -*-
import json
d = json.load(open('src/data/pals.json', encoding='utf-8'))
# Check the 10 suspected empty
suspect = ['pengullet-lux', 'flopie', 'finsider', 'finsider-ignis', 'xenovader', 'xenogard', 'bellanoir', 'bellanoir-libero', 'xenolord', 'hartalis']
for p in d:
    if p['id'] in suspect:
        b = p.get('biomes', [])
        print('%-25s -> %s (truthy=%s)' % (p['id'], b, bool(b)))
