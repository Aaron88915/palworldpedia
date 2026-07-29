#!/usr/bin/env python3
"""检查每页广告位数量（含 Layout 提供的 top+bottom）"""
import os
import re

PAGES_DIR = 'src/pages'
LAYOUT_TOP_PAGES = {'404.astro'}  # showTopAd={false}

# 收集所有 .astro
pages = []
for root, _, files in os.walk(PAGES_DIR):
    for f in files:
        if f.endswith('.astro'):
            pages.append(os.path.join(root, f))

print('=== 每页广告位统计 ===')
print(f'{"页面":<40} {"显式 inline":<12} {"总广告数"}')
print('-' * 70)

for p in sorted(pages):
    rel = os.path.relpath(p, PAGES_DIR)
    content = open(p, encoding='utf-8').read()
    inline = len(re.findall(r'<AdSlot', content))
    layout_top = 0 if rel in LAYOUT_TOP_PAGES else 1
    layout_bottom = 1
    total = inline + layout_top + layout_bottom
    flag = 'OK' if 2 <= total <= 3 else '⚠️'
    print(f'{rel:<40} {inline:<12} {total} {flag}')
