# -*- coding: utf-8 -*-
"""Get FULL HTML and look for Pal Recruiter everywhere."""
import urllib.request, re

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

for name in ['Kingpaca', 'Bellanoir', 'Paladius', 'Frostallion', 'Necromus', 'Jetragon', 'Sibelyx']:
    url = 'https://paldb.cc/en/' + name
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        r = urllib.request.urlopen(req, timeout=20)
        html = r.read().decode('utf-8', errors='ignore')
        open('scripts/_full_%s.html' % name, 'w', encoding='utf-8').write(html)
        # Search for biome-like patterns anywhere
        for needle in ['Pal Recruiter', 'Forest_Volcano', 'Recruiter:', 'pal_recruiter', 'Wild_', 'Map snow', 'Mountaintop', 'Astral', 'Cavern', 'grotto', 'Map yellow', 'Map red', 'Grass 1.', 'Forest 1.', 'Desert_Snow']:
            cnt = html.count(needle)
            if cnt > 0:
                print('%-15s %-30s -> %d' % (name, needle, cnt))
        # Find the "Pal Recruiter" position
        idx = html.find('Pal Recruiter')
        if idx >= 0:
            print('  -> Pal Recruiter at offset %d' % idx)
        print('  -> total length: %d' % len(html))
    except Exception as e:
        print('%s: ERR %s' % (name, e))
    print()
