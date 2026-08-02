#!/usr/bin/env python3
import re
c = open('dist/tech-tree/Accessory_AirDash1/index.html', encoding='utf-8').read()
m = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', c)
if m:
    print('Accessory_AirDash1 dist description:')
    print(f'  {len(m.group(1))} chars')
    print(f'  {m.group(1)}')
