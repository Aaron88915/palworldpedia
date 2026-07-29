# -*- coding: utf-8 -*-
"""Check if combo CSS rules are live on palworldpedia.cc."""
import urllib.request, re

r = urllib.request.urlopen('https://palworldpedia.cc', timeout=15)
d = r.read().decode('utf-8', errors='ignore')
css_links = re.findall(r'href="(/_astro/[^"]+\.css)"', d)
print('CSS files:', css_links)
print()

for css in css_links:
    if 'index' not in css:
        continue
    r2 = urllib.request.urlopen(f'https://palworldpedia.cc{css}', timeout=15)
    css_d = r2.read().decode('utf-8', errors='ignore')
    # Find combo rules
    for m in re.finditer(r'\.combo-parent[^{}]*\{[^}]*\}', css_d):
        print('combo-parent rule:', m.group(0)[:250])
    for m in re.finditer(r'pal-image-wrap[^{}]*\{[^}]*\}', css_d):
        print('pal-image-wrap rule:', m.group(0)[:250])
