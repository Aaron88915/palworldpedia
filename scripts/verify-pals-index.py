# -*- coding: utf-8 -*-
import re
with open('dist/pals/index.html', encoding='utf-8') as f:
    content = f.read()
print(f'Length: {len(content)}')
# Filter rows
rows = re.findall(r'class="filter-label">([^<]+)</span>', content)
print(f'Filter labels: {rows}')
# Check filter chips
chips = re.findall(r'class="chip[^"]*"[^>]*>(.*?)</a>', content, re.DOTALL)
print(f'First 10 chips: {chips[:10]}')
# Active filters
af = re.findall(r'class="active-chip">([^<]+)</a>', content)
print(f'Active filters: {af}')
# Count tiles
tiles = re.findall(r'class="pal-tile"', content)
print(f'Pal tiles: {len(tiles)}')
