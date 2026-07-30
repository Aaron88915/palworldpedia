#!/usr/bin/env python3
import re
files = [
    'dist/index.html',
    'dist/pals/index.html',
    'dist/breeding/index.html',
    'dist/tech-tree/index.html',
    'dist/about/index.html',
]
for f in files:
    try:
        c = open(f, encoding='utf-8').read()
    except FileNotFoundError:
        print(f'{f:<40} NOT FOUND')
        continue
    slots = []
    for m in re.finditer(r'<ins class="adsbygoogle"', c):
        before = c[max(0, m.start()-400):m.start()]
        ad_slot = re.findall(r'ad-slot-(top|bottom|inline|sidebar)', before)
        slots.append(ad_slot[-1] if ad_slot else '?')
    print(f'{f:<40} {len(slots)} ins tags: {slots}')
