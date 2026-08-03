# -*- coding: utf-8 -*-
import re
html = open('scripts/_full_Kingpaca.html', encoding='utf-8').read()
# Find the spawn section (the table with data-pal-id)
# Find all <tr> with data-pal-id
for m in re.finditer(r'<tr[^>]*>(.*?)</tr>', html, re.DOTALL):
    s = m.group(0)
    if 'data-pal-id' in s:
        # Extract pal id and other text
        palid = re.search(r'data-pal-id="([^"]+)"', s)
        # Get all text content
        text = re.sub(r'<[^>]+>', ' ', s)
        text = re.sub(r'\s+', ' ', text).strip()
        if 'KingAlpaca' in s and 'KingAlpaca_Ice' not in s:
            print('KINGPACA row:', text[:200])
            print()
