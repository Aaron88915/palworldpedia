# -*- coding: utf-8 -*-
"""Find medicine-related work keys in palworld.gg."""
import re

with open('scripts/palworldgg-bundles/CK2A4_hG.js', encoding='utf-8') as f:
    d = f.read()

# Find all work-related keys
work_keys = set()
for m in re.finditer(r'work:\{([^}]+)\}', d):
    block = m.group(1)
    for k in re.finditer(r'([A-Z]\w+):(\d+)', block):
        work_keys.add(k.group(1))

print('All work keys in GG:')
for k in sorted(work_keys):
    print(f'  {k}')

# Find what medicine-related keys exist
print('\n=== Medicine-related ===')
for kw in ['Medicine', 'Med', 'Drug', 'Heal', 'Potion']:
    matches = re.findall(rf'({kw}\w*):(\d+)', d)
    if matches:
        print(f'  {kw}*: {len(matches)} matches')
        # Show unique keys
        unique = set(m[0] for m in matches)
        for u in sorted(unique):
            print(f'    {u}')

# Look at Dazzi Noct context specifically
idx = d.find('slug:"dazzi-noct"')
if idx > 0:
    print(f'\n=== Dazzi Noct context ===')
    print(d[idx:idx+1500])
