# -*- coding: utf-8 -*-
"""Inspect what's in paldb.cc for the 10 remaining empty pals."""
import os, re

cache_dir = 'scripts/_paldb_cache'
remaining = [
    ('pengullet-lux', 'Pengullet_Lux'),
    ('flopie', 'Flopie'),
    ('finsider', 'Finsider'),
    ('finsider-ignis', 'Finsider_Ignis'),
    ('xenovader', 'Xenovader'),
    ('xenogard', 'Xenogard'),
    ('bellanoir', 'Bellanoir'),
    ('bellanoir-libero', 'Bellanoir_Libero'),
    ('xenolord', 'Xenolord'),
    ('hartalis', 'Hartalis'),
]

for pid, fname in remaining:
    path = os.path.join(cache_dir, fname + '.html')
    if not os.path.exists(path):
        print('%-25s NOT CACHED' % pid)
        continue
    html = open(path, encoding='utf-8', errors='ignore').read()
    print('--- %s (%d bytes) ---' % (pid, len(html)))
    # Find data-pal-id (internal name)
    palids = re.findall(r'data-pal-id="([^"]+)"', html)
    print('  data-pal-ids: %s' % palids[:5])
    # Find hrefs
    hrefs = re.findall(r'href="([^"]+)"', html)
    # Find spawn-related
    spawners = re.findall(r'spawner=[A-Za-z0-9_]+', html)
    zones = re.findall(r'zone=([a-z_]+)_grade_\d+', html)
    recruiters = re.findall(r'Pal Recruiter:\s*([A-Za-z_]+)', html)
    print('  spawners: %s' % spawners[:5])
    print('  zones: %s' % zones[:3])
    print('  recruiters: %s' % recruiters)
    # Check for "Sealed Realm" / "Wildlife Sanctuary" / specific locations
    for k in ['Sealed_Realm', 'Wildlife_Sanctuary', 'World_Tree_Holy_Water', 'Palpagos_Islands?pos=', 'Incident', 'Alpha']:
        cnt = html.count(k)
        if cnt > 0:
            print('  found %s: %d' % (k, cnt))
    # Check for any text near boss/tower mentions
    for k in ['Tower', 'Rampaging', 'Boss', 'Alpha']:
        idx = html.find(k)
        if idx > 0:
            snippet = html[max(0, idx-100):idx+200]
            snippet = re.sub(r'<[^>]+>', ' ', snippet)
            snippet = re.sub(r'\s+', ' ', snippet)
            if 'css' not in snippet and 'script' not in snippet:
                print('  near %s: %s' % (k, snippet[:200]))
    print()
