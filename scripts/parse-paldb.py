# -*- coding: utf-8 -*-
import urllib.request, re

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

req = urllib.request.Request('https://paldb.cc/en/Lamball', headers=HEADERS)
r = urllib.request.urlopen(req, timeout=15)
data = r.read().decode('utf-8', errors='ignore')

# Find Pal Recruiter section
m = re.search(r'Pal Recruiter(.*?)(?=<h[1-6]|<section|<div class="col-12">)', data, re.DOTALL)
if m:
    text = re.sub(r'<[^>]+>', ' ', m.group(1))
    text = re.sub(r'\s+', ' ', text).strip()
    print('Pal Recruiter section:')
    print(text[:2000])
print()
# Find Wild Spawn or similar
for kw in ['Wild Spawn', 'Wild', 'Habitat', 'Location', 'Where to find']:
    idx = data.find(kw)
    if idx > 0:
        # Get 1500 chars context
        chunk = data[idx:idx+2500]
        text = re.sub(r'<[^>]+>', ' ', chunk)
        text = re.sub(r'\s+', ' ', text).strip()
        print(f'\n=== "{kw}" at {idx} ===')
        print(text[:1500])
        break
