#!/usr/bin/env python3
import re
for f in ['dist/calculator/power/index.html', 'dist/tech-tree/AIcore/index.html', 'dist/tech-tree/AncientArmor/index.html']:
    c = open(f, encoding='utf-8').read()
    m = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', c)
    if m: print(f'{f}:\n  {m.group(1)}\n')
