# -*- coding: utf-8 -*-
"""Show what was filled by paldb.cc and what's still empty."""
import json, os, re

pals = json.load(open('src/data/pals.json', encoding='utf-8'))
by_id = {p['id']: p for p in pals}

# Check cache for pals that are still empty
empty = [p for p in pals if not p.get('biomes')]
print('Still empty: %d' % len(empty))
for p in empty:
    pid = p['id']
    paldb_name = ' '.join(s.capitalize() for s in pid.split('-'))
    cache_path = os.path.join('scripts/_paldb_cache', paldb_name.replace(' ', '_') + '.html')
    if not os.path.exists(cache_path):
        print('  NO CACHE: %s' % pid)
        continue
    html = open(cache_path, encoding='utf-8', errors='ignore').read()
    # Look for any biome hints
    hints = []
    # 1. spawner zones
    for m in re.finditer(r'spawner=[A-Za-z0-9_]*?(grass|forest|desert|dessert|snow|volcano|dark|sky|moon|feybreak|sakurajima|sanctuary)[A-Za-z0-9_]*', html):
        hints.append(('spawner-zone', m.group(1)))
    # 2. zone=
    for m in re.finditer(r'zone=([a-z][a-z0-9]*)_grade_\d+', html):
        hints.append(('zone', m.group(1)))
    # 3. World_Tree_Holy_Water
    if 'World_Tree_Holy_Water' in html:
        hints.append(('world_tree', ''))
    if 'Wildlife_Sanctuary' in html:
        hints.append(('wildlife_sanctuary', ''))
    if 'Sealed_Realm' in html:
        hints.append(('sealed_realm', ''))
    if 'Pal_Recruiter' in html:
        # find what biome
        for m in re.finditer(r'Pal Recruiter:\s*([A-Za-z_]+)', html):
            hints.append(('pal_recruiter', m.group(1)))
    if 'Rampaging' in html:
        hints.append(('rampaging', ''))
    if 'Tower' in html:
        hints.append(('tower', ''))
    if 'Dungeons' in html:
        hints.append(('dungeons', ''))
    print('  %-25s hints: %s' % (pid, hints[:8]))
