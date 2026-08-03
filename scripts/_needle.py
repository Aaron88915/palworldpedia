# -*- coding: utf-8 -*-
import re
html = open('scripts/_full_Kingpaca.html', encoding='utf-8').read()
print('Total size:', len(html))
print('body close idx:', html.rfind('</body>'))
for needle in ['Wild Spawn', 'Pal Recruiter', 'Pal Recruiter:', 'pal_recruiter', 'Incident', 'MapName', 'Daytime', 'Night', 'MapArea', 'Biome', 'biome', 'T_KingAlpaca_Ice']:
    idx = html.find(needle)
    if idx > 0:
        print('%-25s at %d' % (needle, idx))

# Find the data table area
m = re.search(r'class="table.{0,5000}', html, re.DOTALL)
if m:
    s = re.sub(r'<[^>]+>', ' ', m.group(0))
    s = re.sub(r'\s+', ' ', s)
    print('Table found:')
    print(s[:2000])
