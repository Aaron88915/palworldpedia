#!/usr/bin/env python3
import re
files = [
    'dist/index.html',
    'dist/pals/index.html',
    'dist/breeding/index.html',
    'dist/tech-tree/index.html',
]
for f in files:
    c = open(f, encoding='utf-8').read()
    print(f'\n=== {f} ===')
    # 找所有 ad-slot
    for m in re.finditer(r'ad-slot-(top|bottom|inline|sidebar)', c):
        around = c[max(0, m.start()-50):min(len(c), m.end()+200)]
        around = re.sub(r'\s+', ' ', around)[:250]
        print(f'  @{m.start()}: ...{around}...')
