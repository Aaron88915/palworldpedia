# -*- coding: utf-8 -*-
"""Find pal data in CK2A4_hG.js bundle - look for image URLs."""
import re

with open('scripts/palworldgg-bundles/CK2A4_hG.js', encoding='utf-8') as f:
    d = f.read()
print(f'Bundle size: {len(d)}')

# Find image URLs (cloudfront/cloudinary/etc)
img_urls = set(re.findall(r'https?://[^\s"\'<>]+\.(?:webp|png|jpg|jpeg|avif)', d))
print(f'Image URLs: {len(img_urls)}')
for u in sorted(img_urls)[:10]:
    print(f'  {u}')

# Look for Fuack in the data
for name in ['Fuack', 'Tanzee', 'Clovee', 'Panthalus', 'Dumud Gild']:
    idx = d.find(f'name:"{name}"')
    if idx > 0:
        ctx = d[max(0,idx-50):idx+800]
        print(f'\n=== {name} ===')
        print(ctx[:600])
