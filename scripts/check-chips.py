# -*- coding: utf-8 -*-
import re
with open('dist/pals/index.html', encoding='utf-8') as f:
    content = f.read()
chips = re.findall(r'<a href="(/pals/\?[^"]+)"[^>]*>([^<]+)</a>', content)
print(f'Filter chips with query params: {len(chips)}')
for href, label in chips[:10]:
    print(f'  {href} -> {label.strip()}')
