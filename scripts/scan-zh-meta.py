#!/usr/bin/env python3
import os, re

print('=== ZH 页 description 长度检查 ===')
short_ones = []
long_ones = []
for root, _, files in os.walk('dist'):
    # 只看根（不是 /en/ 子树）
    if root.startswith('dist/en') or '\\en\\' in root:
        continue
    for f in files:
        if not f.endswith('.html'):
            continue
        path = os.path.join(root, f)
        c = open(path, encoding='utf-8').read()
        m = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', c)
        if m:
            text = m.group(1)
            rel = os.path.relpath(path, 'dist')
            if len(text) < 70:
                short_ones.append((rel, len(text), text))
            if len(text) > 160:
                long_ones.append((rel, len(text), text))

print(f'ZH 过短 (<70): {len(short_ones)}')
for rel, l, t in short_ones[:10]:
    print(f'  {rel:<50} {l} chars')
    print(f'    {t}')
print(f'\nZH 超长 (>160): {len(long_ones)}')
for rel, l, t in long_ones[:10]:
    print(f'  {rel:<50} {l} chars')
