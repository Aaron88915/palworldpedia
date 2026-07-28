# -*- coding: utf-8 -*-
"""Download CK2A4_hG.js which has the actual pal data."""
import urllib.request, os

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
url = 'https://palworld.gg/_nuxt/CK2A4_hG.js'
req = urllib.request.Request(url, headers=HEADERS)
d = urllib.request.urlopen(req, timeout=30).read()
print(f'Size: {len(d)}')
with open('scripts/palworldgg-bundles/CK2A4_hG.js', 'wb') as f:
    f.write(d)
