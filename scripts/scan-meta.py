#!/usr/bin/env python3
import os, re

print('=== 英文页 meta description 长度检查 ===')
long_ones = []
for root, _, files in os.walk('dist/en'):
    for f in files:
        if not f.endswith('.html'):
            continue
        path = os.path.join(root, f)
        c = open(path, encoding='utf-8').read()
        m = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', c)
        if m:
            text = m.group(1)
            rel = os.path.relpath(path, 'dist/en')
            if len(text) > 160:
                long_ones.append((rel, len(text), text))

print(f'Total too long (>160): {len(long_ones)}')
for rel, length, text in sorted(long_ones, key=lambda x: -x[1])[:15]:
    print(f'  {rel:<50} {length} chars')
    print(f'    {text[:120]}...')
    print()
