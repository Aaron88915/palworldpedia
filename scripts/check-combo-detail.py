# -*- coding: utf-8 -*-
"""Check combo section in detail - all images and sizes."""
import urllib.request, re

r = urllib.request.urlopen('https://palworldpedia.cc', timeout=15)
d = r.read().decode('utf-8', errors='ignore')

# Find all pal-image-wrap elements
wraps = re.findall(r'<div class="pal-image-wrap[^>]+>', d)
print(f'Total pal-image-wrap elements: {len(wraps)}')

# Check if all combos use combo-parent or combo-child
combo_section_match = re.search(r'<h2[^>]*>🧬 热门配种公式</h2>(.*?)<h2', d, re.DOTALL)
if combo_section_match:
    section = combo_section_match.group(1)
    wraps_in_section = re.findall(r'<div class="pal-image-wrap[^>]+>', section)
    print(f'Pal-image-wraps in combo section: {len(wraps_in_section)}')

    # Count combo-parent and combo-child
    parents = re.findall(r'<div class="combo-parent[^>]*>', section)
    children = re.findall(r'<div class="combo-child[^>]*>', section)
    print(f'combo-parent cells: {len(parents)}')
    print(f'combo-child cells: {len(children)}')

    # Look for any image NOT inside combo-parent or combo-child
    all_imgs = re.findall(r'<img[^>]+>', section)
    print(f'Total imgs in combo section: {len(all_imgs)}')

# Also check the full HTML output for the combo section (first 2000 chars)
if combo_section_match:
    print()
    print('--- First 2000 chars of combo section HTML ---')
    print(combo_section_match.group(1)[:2000])
