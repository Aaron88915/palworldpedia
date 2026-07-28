# -*- coding: utf-8 -*-
"""Probe paldb.cc to find the rarity HTML structure."""
import urllib.request, re

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

for slug in ['Jetragon', 'Lamball', 'Mau', 'Cattiva', 'Panthalus', 'Rayhound']:
    url = f'https://paldb.cc/en/{slug}'
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        r = urllib.request.urlopen(req, timeout=20)
        d = r.read().decode('utf-8', errors='ignore')
        # Find the Rarity section
        m = re.search(r'Rarity', d)
        if m:
            idx = m.start()
            # Get the surrounding 500 chars
            ctx = d[max(0, idx-200):idx+500]
            # Strip excessive whitespace
            ctx = re.sub(r'\s+', ' ', ctx)
            print(f'\n=== {slug} ===')
            print(ctx)
    except Exception as e:
        print(f'  {slug}: ERR {e}')
