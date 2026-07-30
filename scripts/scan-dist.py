#!/usr/bin/env python3
import re
files = [
    'dist/index.html',
    'dist/pals/index.html',
    'dist/breeding/index.html',
    'dist/tech-tree/index.html',
    'dist/about/index.html',
    'dist/contact/index.html',
    'dist/terms/index.html',
]
for f in files:
    c = open(f, encoding='utf-8').read()
    # 找所有 ad-slot-XXX 出现的位置
    classes = re.findall(r'ad-slot-(\w+)', c)
    counts = {}
    for cls in classes:
        counts[cls] = counts.get(cls, 0) + 1
    print(f'{f:<40} {counts}')
