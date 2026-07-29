# -*- coding: utf-8 -*-
"""Extract breeding data from HCkNB-ax.js."""
import re

with open('scripts/palworldgg-bundles/HCkNB-ax.js', 'r', encoding='utf-8') as f:
    d = f.read()

print(f'Bundle size: {len(d)}')

# Find array definitions with pal names
# Pattern: [..., {name:"Lamball", ...}, ...]
# Or: [..., ["Lamball", ...], ...]
# Look for the structure that has many pal names

# Find all occurrences of "Lamball"
for m in re.finditer(r'[\"\']Lamball[\"\']', d):
    idx = m.start()
    print(f'\n--- Lamball @ {idx} ---')
    print(d[max(0,idx-300):idx+500])

# Find common pal arrays
for m in re.finditer(r'\[("Mau"|"Cattiva"|"Lamball")', d):
    idx = m.start()
    print(f'\n--- Array @ {idx} ---')
    print(d[max(0,idx-200):idx+1000])
