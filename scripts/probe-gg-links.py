# -*- coding: utf-8 -*-
"""Find pal page URL pattern on palworld.gg."""
import urllib.request, re

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

# Get homepage and find pal links
req = urllib.request.Request('https://palworld.gg/pals', headers=HEADERS)
r = urllib.request.urlopen(req, timeout=20)
d = r.read().decode('utf-8', errors='ignore')
print(f'Homepage len: {len(d)}')

# Find all pal page links
links = re.findall(r'href="(/pals/[^"]+)"', d)
unique = sorted(set(links))
print(f'Unique pal links: {len(unique)}')
print('First 20:')
for l in unique[:20]:
    print(f'  {l}')
