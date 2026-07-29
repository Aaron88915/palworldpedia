# -*- coding: utf-8 -*-
"""Fetch the JS bundle and look for API endpoints / data URLs."""
import urllib.request, re

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

# Get main page to find bundles
url = 'https://palworld.gg/breeding-calculator'
req = urllib.request.Request(url, headers=HEADERS)
data = urllib.request.urlopen(req, timeout=20).read().decode('utf-8', errors='ignore')

# Find all _nuxt/ JS files
scripts = re.findall(r'/_nuxt/([\w\-]+\.js)', data)
print('JS bundles:', scripts)

# Look in the main one (usually the longest)
import os
os.makedirs('scripts/palworldgg-bundles', exist_ok=True)
all_endpoints = set()
for s in scripts[:8]:
    u = f'https://palworld.gg/_nuxt/{s}'
    print(f'\n=== {u} ===')
    try:
        req2 = urllib.request.Request(u, headers=HEADERS)
        d = urllib.request.urlopen(req2, timeout=20).read().decode('utf-8', errors='ignore')
        print(f'  size={len(d)}')
        with open(f'scripts/palworldgg-bundles/{s}', 'w', encoding='utf-8') as f:
            f.write(d)
        # Find data endpoints
        for kw in ['/api/', 'palworld.gg/', '.json', 'breed', 'paldata', 'paldex']:
            for m in re.finditer(rf'[\"\']{{1}}([^\"\']*{re.escape(kw)}[^\"\']*?)[\"\']{{1}}', d):
                ep = m.group(1)
                if ep.startswith('http') or ep.startswith('/'):
                    all_endpoints.add(ep)
    except Exception as e:
        print(f'  ERR: {e}')

print(f'\n--- All endpoints ({len(all_endpoints)}) ---')
for ep in sorted(all_endpoints)[:40]:
    print(f'  {ep}')
