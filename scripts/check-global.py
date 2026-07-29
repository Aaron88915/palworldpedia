# -*- coding: utf-8 -*-
"""Check if :global fix is live."""
import urllib.request, re

r = urllib.request.urlopen('https://palworldpedia.cc', timeout=15)
d = r.read().decode('utf-8', errors='ignore')
css = re.findall(r'href="(/_astro/[^"]+\.css)"', d)
for c in css:
    if 'index' in c:
        cd = urllib.request.urlopen(f'https://palworldpedia.cc{c}', timeout=15).read().decode('utf-8', errors='ignore')
        # Check the new combo CSS
        for m in re.finditer(r'combo-icon\{[^}]*\}', cd):
            print('ICON:', m.group(0)[:300])
        for m in re.finditer(r'combo-icon-child\{[^}]*\}', cd):
            print('CHILD:', m.group(0)[:300])
        # Check for important
        for m in re.finditer(r'pal-image-wrap\{[^}]*\}', cd):
            print('WRAP:', m.group(0)[:200])
            break
