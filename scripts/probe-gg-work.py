# -*- coding: utf-8 -*-
"""Look at a specific pal's work block."""
import re

with open('scripts/palworldgg-bundles/CK2A4_hG.js', encoding='utf-8') as f:
    d = f.read()

# Find Orserk's block
m = re.search(r'slug:"orserk"[^}]*?work:\{([^}]+)\}', d)
if m:
    print(f'Orserk work block: {m.group(1)[:500]}')
else:
    # Try simpler - just look for Orserk
    idx = d.find('slug:"orserk"')
    if idx > 0:
        print('Orserk context (2000 chars):')
        print(d[idx:idx+2000])

# Also try a specific name
print('\n\n=== Grizzbolt context ===')
idx = d.find('slug:"grizzbolt"')
if idx > 0:
    print(d[idx:idx+2000])
