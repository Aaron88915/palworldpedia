# -*- coding: utf-8 -*-
"""Try different URL patterns for paldb.cc."""
import urllib.request, urllib.parse, os, re

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

# Try these URL patterns for Wixen Noct (which we know works from existing data)
test = [
    'Wixen_Noct', 'Wixen-Noct', 'WixenNoct', 'Wixen%20Noct',
    'Pengullet_Lux', 'Pengullet-Lux', 'PengulletLux',
    'Faleris_Aqua', 'Faleris-Aqua',
    'Nitemary_Botan', 'Nitemary-Botan',
    'Jormuntide_Ignis', 'Jormuntide-Ignis',
    'Suzaku_Aqua',
    'Jetragon',
    'Neptilius',
    'Panthalus',
    'Grizzbolt',
    'Orserk',
]

for n in test:
    url = 'https://paldb.cc/en/' + n
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        r = urllib.request.urlopen(req, timeout=15)
        html = r.read().decode('utf-8', errors='ignore')
        # Check if it has actual content
        has_recruiter = 'Pal Recruiter' in html
        has_spawner = 'spawner=' in html
        size = len(html)
        print('%-25s OK %d bytes | recruiter=%s spawner=%s' % (n, size, has_recruiter, has_spawner))
        # Save it
        with open('scripts/_paldb_cache/' + n + '.html', 'w', encoding='utf-8', errors='ignore') as f:
            f.write(html)
    except Exception as e:
        print('%-25s ERR %s' % (n, str(e)[:50]))
