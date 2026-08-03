# -*- coding: utf-8 -*-
"""Probe paldb.cc HTML to see what's there for Kingpaca."""
import urllib.request, re

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

for name in ['Kingpaca', 'Flopie', 'Bellanoir', 'Frostallion', 'Paladius', 'Loupmoon', 'Sibelyx']:
    url = 'https://paldb.cc/en/' + name
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        r = urllib.request.urlopen(req, timeout=20)
        html = r.read().decode('utf-8', errors='ignore')
        # Save first 2000 chars
        open('scripts/_full_%s.html' % name, 'w', encoding='utf-8').write(html[:3000])
        # Also look for any "Recruiter" or "Biome" string
        for needle in ['Pal Recruiter', 'Recruiter', 'biome', 'Biome', 'Wild', '(Wild)', 'Map ']:
            cnt = html.count(needle)
            print('%-15s %-15s -> %d' % (name, needle, cnt))
    except Exception as e:
        print('%s: ERR %s' % (name, e))
    print()
