# -*- coding: utf-8 -*-
import json
d = json.load(open('src/data/pals.json', encoding='utf-8'))

# pals with biomes
rows = []
for p in d:
    if p.get('biomes'):
        rows.append('%-30s paldeckNo=%-3d types=%-30s rarity=%-2d night=%-5s -> %s' % (
            p['id'],
            p.get('paldeckNo', 0),
            ','.join(p.get('types', [])),
            p.get('rarity', 0),
            str(p.get('nightOnly', False)),
            p['biomes'],
        ))
open('scripts/_pals_with_biomes.txt', 'w', encoding='utf-8').write('\n'.join(rows))
print('wrote _pals_with_biomes.txt (%d rows)' % len(rows))

# pals without biomes
rows = []
for p in d:
    if not p.get('biomes'):
        rows.append('%-30s paldeckNo=%-3d types=%-30s rarity=%-2d night=%-5s' % (
            p['id'],
            p.get('paldeckNo', 0),
            ','.join(p.get('types', [])),
            p.get('rarity', 0),
            str(p.get('nightOnly', False)),
        ))
open('scripts/_pals_no_biomes.txt', 'w', encoding='utf-8').write('\n'.join(rows))
print('wrote _pals_no_biomes.txt (%d rows)' % len(rows))
