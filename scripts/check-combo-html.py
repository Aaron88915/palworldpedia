# -*- coding: utf-8 -*-
"""Check the rendered combo HTML to see if image sizes are 48px."""
import urllib.request, re

r = urllib.request.urlopen('https://palworldpedia.cc', timeout=15)
d = r.read().decode('utf-8', errors='ignore')

# Find combo-row sections
combo_rows = re.findall(r'<div class="combo-row[^>]*>.*?</div>\s*</div>\s*</div>', d, re.DOTALL)
print(f'Found {len(combo_rows)} combo rows')
print()

for i, row in enumerate(combo_rows[:3]):
    print(f'=== Combo {i+1} ===')
    # Find image src
    imgs = re.findall(r'<img[^>]+src="[^"]+"', row)
    for img in imgs[:3]:
        print(f'  IMG: {img[:200]}')
    # Find combo-parent names
    parents = re.findall(r'<div class="combo-parent[^>]*>(.*?)</div>', row, re.DOTALL)
    for p in parents:
        # Get pal name
        name_match = re.search(r'<span[^>]*>([^<]+)</span>', p)
        if name_match:
            print(f'  Parent: {name_match.group(1)}')
    print()
