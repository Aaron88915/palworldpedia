# -*- coding: utf-8 -*-
import json, os, re

dist_files = [
    'dist/pals/gumoss-special/index.html',
    'dist/pals/cryolinx-terra/index.html',
    'dist/pals/lamball/index.html',
]

for path in dist_files:
    print(f'=== {path} ===')
    print('  exists:', os.path.exists(path))
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            content = f.read()
        print(f'  length: {len(content)}')
        # Look for stat values
        for m in re.finditer(r'class="stat-value">([^<]*)</div>', content):
            print(f'  stat-value: {m.group(1)!r}')
        for m in re.finditer(r'class="stat-label">([^<]*)</div>', content):
            print(f'  stat-label: {m.group(1)!r}')
        for m in re.finditer(r'<h2[^>]*>([^<]+)</h2>', content):
            print(f'  h2: {m.group(1)!r}')
    print()
