# -*- coding: utf-8 -*-
import re
html = open('scripts/_full_Kingpaca.html', encoding='utf-8').read()
positions = [m.start() for m in re.finditer(r'data-pal-id', html)]
# Show context around each (no truncation)
for pos in positions:
    snippet = html[max(0, pos-100):pos+800]
    text = re.sub(r'<[^>]+>', ' ', snippet)
    text = re.sub(r'\s+', ' ', text).strip()
    print('At %d: %s' % (pos, text))
    print('---')
