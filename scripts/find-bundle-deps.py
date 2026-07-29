# -*- coding: utf-8 -*-
"""Find external imports and data URLs from Crnsudxy.js."""
import re

with open('scripts/palworldgg-bundles/Crnsudxy.js', 'r', encoding='utf-8') as f:
    d = f.read()

# Look for import() / dynamic imports
# Look for /api/ paths
print('--- /api/ or .json in main bundle ---')
for kw in ['.json', '/api/', 'palworld.cc', 'palworldgg', 'breed', 'cdn.']:
    for m in re.finditer(rf'[\"\'](/[^\"\']*{re.escape(kw)}[^\"\']*|https?://[^\"\']*{re.escape(kw)}[^\"\']*)', d):
        ep = m.group(1)
        if len(ep) < 200:
            print(f'  [{kw}] {ep}')

# Look for any URL strings
print('\n--- All https URLs in main bundle ---')
urls = set(re.findall(r'https?://[^\s\"\'<>]+', d))
for u in sorted(urls)[:40]:
    print(f'  {u}')

# Look for all _nuxt/ refs (other bundles)
print('\n--- _nuxt/ refs ---')
nuxt_refs = set(re.findall(r'/_nuxt/[\w\-./]+', d))
for u in sorted(nuxt_refs):
    print(f'  {u}')
