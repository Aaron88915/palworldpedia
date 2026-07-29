# -*- coding: utf-8 -*-
import re
with open('dist/pals/index.html', encoding='utf-8') as f:
    content = f.read()
# Find filter-row
m = re.search(r'class="filter-row"[^>]*>(.*?)</div>\s*</div>', content, re.DOTALL)
if m:
    print(m.group(0)[:2000])
