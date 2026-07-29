# -*- coding: utf-8 -*-
import re
with open('dist/pals/index.html', encoding='utf-8') as f:
    content = f.read()
# Check a sample tile
m = re.search(r'<a href="/pals/lifmunk/"\s+class="pal-tile"\s+([^>]+)>', content)
if m:
    print('Sample tile attributes (Lifmunk):')
    print('  ' + m.group(1))
print()
# Count tiles with data attributes
data_tiles = re.findall(r'class="pal-tile"\s+data-id=', content)
print(f'Tiles with data-id: {len(data_tiles)}')
# Check chips are buttons now
buttons = re.findall(r'<button type="button" data-filter-value="(\w*)"', content)
print(f'Filter buttons: {len(buttons)}, unique values: {len(set(buttons))}')
# Check no leftover <a href="/pals/?type=...
old_chips = re.findall(r'href="/pals/\?type=', content)
print(f'Old <a href> chips remaining: {len(old_chips)}')
