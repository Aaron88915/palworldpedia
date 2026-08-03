# -*- coding: utf-8 -*-
import re
html = open('scripts/_full_Kingpaca.html', encoding='utf-8').read()
# Look for all tr that contain KingAlpaca (and not the _Ice variant)
trs = re.findall(r'<tr[^>]*>.*?</tr>', html, re.DOTALL)
print('Total trs:', len(trs))
for tr in trs:
    if 'KingAlpaca' in tr and 'KingAlpaca_Ice' not in tr:
        text = re.sub(r'<[^>]+>', ' ', tr)
        text = re.sub(r'\s+', ' ', text).strip()
        if 'Kingpaca' in text or 'KingAlpaca' in text:
            print('TR:', text[:300])
            print()
