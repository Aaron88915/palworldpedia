#!/usr/bin/env python3
import re
c = open('dist/index.html', encoding='utf-8').read()
m = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', c)
if m:
    print(f'ZH description: {len(m.group(1))} chars')
    print(m.group(1))
