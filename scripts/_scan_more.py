# -*- coding: utf-8 -*-
"""Check various paldb.cc pages for spawn data patterns."""
import re, os

cache_dir = 'scripts/_paldb_cache'
files = sorted(os.listdir(cache_dir))
print('Cached files (%d):' % len(files))
for fn in files[:30]:
    print('  %s' % fn)
print()

# Check some pages for what's in them
for name in ['Frostallion', 'Paladius', 'Necromus', 'Bellanoir', 'Jetragon', 'Grizzbolt', 'Orserk', 'Faleris', 'Kingpaca', 'Flopie', 'Icelyn', 'Whalaska', 'Faleris_Aqua', 'Nitemary_Botan']:
    path = os.path.join(cache_dir, name + '.html')
    if not os.path.exists(path):
        print('%-25s NOT CACHED' % name)
        continue
    html = open(path, encoding='utf-8', errors='ignore').read()
    # find all hrefs that might be relevant
    hrefs = re.findall(r'href="([^"]+)"', html)
    relevant = [h for h in hrefs if any(k in h.lower() for k in ['island', 'world', 'spawner', 'pos', 'recruiter', 'forest', 'snow', 'volcano', 'grass', 'desert', 'cave', 'realm', 'sanctuary', 'mountain', 'feybreak', 'sakurajima', 'incidentspawner'])]
    print('%-25s %d hrefs' % (name, len(relevant)))
    for h in relevant[:8]:
        print('  ', h)
    print()
