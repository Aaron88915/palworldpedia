# -*- coding: utf-8 -*-
"""Trace what parse_biomes does for Finsider."""
import sys
sys.path.insert(0, 'scripts')

# Read the script source and execute it
src = open('scripts/fill-biomes.py', encoding='utf-8').read()
# Extract just the parse function
import re
m = re.search(r'PALDB_BIOME_ID_MAP\s*=\s*\{[^}]+\}', src, re.DOTALL)
print('Has PALDB_BIOME_ID_MAP:', bool(m))

# Just run the script and check
exec(src)

# Now check
import json
d = json.load(open('src/data/pals.json', encoding='utf-8'))
for p in d:
    if p['id'] in ('finsider', 'flopie', 'pengullet-lux'):
        print('%-25s -> %s' % (p['id'], p.get('biomes', [])))
