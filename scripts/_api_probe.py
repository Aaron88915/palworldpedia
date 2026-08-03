# -*- coding: utf-8 -*-
import re
html = open('scripts/_full_Kingpaca.html', encoding='utf-8').read()
print('Length:', len(html))
# Look for any URL that might be an API call
for m in re.finditer(r'(https?://[^\"\s\']+|/api/[^\"\s\']+|fetch\([\"\'][^\"\']+|axios\.[a-z]+\([\"\']([^\"\']+)|url:\s*[\"\']([^\"\']+))', html):
    print('API?:', m.group(0)[:200])
# Also look for any "Location" or spawn info
for needle in ['Location', 'Spawn', 'Pal Recruiter', 'Biome', 'biome', 'Incident', 'palbox', 'wild', 'Wild']:
    for m in re.finditer(r'.{0,80}' + needle + r'.{0,200}', html):
        s = m.group(0)
        s = re.sub(r'<[^>]+>', ' ', s)
        s = re.sub(r'\s+', ' ', s)
        if 'css' in s.lower() or 'script' in s.lower():
            continue
        print('%-15s context: %s' % (needle, s[:300]))
        break
