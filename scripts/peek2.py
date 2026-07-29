# -*- coding: utf-8 -*-
import re

for path in ['dist/pals/gumoss-special/index.html', 'dist/pals/cryolinx-terra/index.html']:
    with open(path, encoding='utf-8') as f:
        content = f.read()
    print(f'=== {path} (len={len(content)}) ===')
    # Find any stat-related string
    idx = content.find('stat-')
    if idx > 0:
        print(f'  stat- at {idx}: ...{content[idx-30:idx+500]}...')
    idx = content.find('stat-value')
    if idx > 0:
        print(f'  stat-value at {idx}: ...{content[idx-50:idx+400]}...')
    # Find all h2
    h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', content, re.DOTALL)
    print(f'  h2s: {h2s}')
    # Find all "data-astro-cid"
    print('--- end ---')
    print()
