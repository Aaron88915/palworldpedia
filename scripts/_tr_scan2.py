# -*- coding: utf-8 -*-
import re
html = open('scripts/_full_Kingpaca.html', encoding='utf-8').read()
# Look for all tr that contain KingAlpaca
trs = re.findall(r'<tr[^>]*>.*?</tr>', html, re.DOTALL)
print('Total trs:', len(trs))
for i, tr in enumerate(trs):
    text = re.sub(r'<[^>]+>', ' ', tr)
    text = re.sub(r'\s+', ' ', text).strip()
    print('TR %d: %s' % (i, text[:300]))
    print()
