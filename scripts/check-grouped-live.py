# -*- coding: utf-8 -*-
"""Check if grouped view CSS/JS is live."""
import urllib.request, re

r = urllib.request.urlopen('https://palworldpedia.cc/pals/', timeout=15)
d = r.read().decode('utf-8', errors='ignore')

# Look for the new CSS rules
css_links = re.findall(r'href="(/_astro/[^"]+\.css)"', d)
for c in css_links:
    if 'index' in c and 'about' not in c:
        cd = urllib.request.urlopen(f'https://palworldpedia.cc{c}', timeout=15).read().decode('utf-8', errors='ignore')
        if 'group-header' in cd:
            print(f'  {c}: group-header CSS live')
            # Show sample rule
            m = re.search(r'\.group-header[^{]*\{[^}]*\}', cd)
            if m:
                print(f'    {m.group(0)[:200]}')
        if 'view-grouped' in cd:
            print(f'  {c}: view-grouped CSS live')
        if 'groupTilesByType' in d or 'groupTilesByType' in cd:
            print('  groupTilesByType JS live')
        break
