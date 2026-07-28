# -*- coding: utf-8 -*-
import re
with open('scripts/palworldgg-bundles/CK2A4_hG.js', encoding='utf-8') as f:
    d = f.read()
for kw in ['Gumoss', 'gumoss', 'Slime', 'Special', 'Yakushima']:
    for m in re.finditer(rf'(?:name|slug):"([^"]*{re.escape(kw)}[^"]*)"', d):
        print(f'  [{kw}] {m.group(1)}')
