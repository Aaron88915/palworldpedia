# -*- coding: utf-8 -*-
"""Find image URL pattern from homepage HTML."""
import urllib.request, re

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
req = urllib.request.Request('https://palworld.gg/pals', headers=HEADERS)
d = urllib.request.urlopen(req, timeout=20).read().decode('utf-8', errors='ignore')

# Find any image src containing pal texture name
for kw in ['T_BluePlatypus', 'T_Monkey', 'T_KingWhale', 'T_CloverFairy']:
    for m in re.finditer(rf'(?:src|data-src)=["\']([^"\']*{re.escape(kw)}[^"\']*)["\']', d):
        print(f'  {m.group(1)[:250]}')
        break

# Also look for any image pattern in /images/ or /palworld/
imgs = re.findall(r'(?:src|data-src)=["\']([^"\']*\.(?:webp|png|jpg|jpeg))["\']', d)
print(f'\nTotal imgs: {len(imgs)}')
for u in imgs[:10]:
    print(f'  {u[:200]}')
