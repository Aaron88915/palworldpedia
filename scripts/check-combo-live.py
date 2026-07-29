# -*- coding: utf-8 -*-
import urllib.request, re

r = urllib.request.urlopen('https://palworldpedia.cc', timeout=15)
d = r.read().decode('utf-8', errors='ignore')
css = re.findall(r'href="(/_astro/[^"]+\.css)"', d)
for c in css:
    if 'index' in c:
        cd = urllib.request.urlopen(f'https://palworldpedia.cc{c}', timeout=15).read().decode('utf-8', errors='ignore')
        # Look for combo rules
        keywords = ['combo-row', 'combo-pals', 'combo-parent', 'combo-child', 'pal-image-wrap']
        for kw in keywords:
            idx = cd.find(kw)
            if idx > 0:
                ctx = cd[max(0, idx-30):idx+150]
                print(f'[{kw}]: {ctx[:200]}')
                print()
