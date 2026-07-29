# -*- coding: utf-8 -*-
"""Check if equation pill CSS is live."""
import urllib.request, re

r = urllib.request.urlopen('https://palworldpedia.cc', timeout=15)
d = r.read().decode('utf-8', errors='ignore')
css = re.findall(r'href="(/_astro/[^"]+\.css)"', d)
for c in css:
    if 'index' in c:
        cd = urllib.request.urlopen(f'https://palworldpedia.cc{c}', timeout=15).read().decode('utf-8', errors='ignore')
        # Check for combo-row and combo-icon styles
        for kw in ['combo-row', 'combo-icon', 'combo-tooltip']:
            idx = cd.find(kw)
            if idx > 0:
                print(f'[{kw}]: {cd[idx:idx+200]}')
                print()
        # Also check for the new pill shape
        if 'border-radius:999px' in cd:
            print('  → pill border-radius:999px present')
        break
