# -*- coding: utf-8 -*-
import re
html = open('scripts/_full_Kingpaca.html', encoding='utf-8').read()
# Find spawn-related content (data-pal-id)
# data-pal-id pattern
positions = [m.start() for m in re.finditer(r'data-pal-id', html)]
print('Number of data-pal-id occurrences:', len(positions))
# Show context around each
for pos in positions[:5]:
    snippet = html[max(0, pos-100):pos+500]
    text = re.sub(r'<[^>]+>', ' ', snippet)
    text = re.sub(r'\s+', ' ', text).strip()
    print('At %d: %s' % (pos, text[:400]))
    print()
