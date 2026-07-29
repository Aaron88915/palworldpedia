# -*- coding: utf-8 -*-
import urllib.request, re

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

req = urllib.request.Request('https://paldb.cc/en/Lamball', headers=HEADERS)
r = urllib.request.urlopen(req, timeout=15)
data = r.read().decode('utf-8', errors='ignore')

# Find the section starting with "(Wild)" - these are wild spawns
wild_start = data.find('(Wild)')
print(f'(Wild) at: {wild_start}')
# Get 3000 chars
chunk = data[wild_start-500:wild_start+5000]
# Strip HTML
text = re.sub(r'<[^>]+>', ' ', chunk)
text = re.sub(r'\s+', ' ', text).strip()
print('Context around (Wild):')
print(text[:3000])
print()
# Look for "Dawn" / "Night" patterns (these indicate Nocturnal or day/night)
print('---')
# Find "Breeding Combos" / "Parents"
for kw in ['Breeding', 'Parents', 'Parent', 'Daytime', 'Nighttime']:
    idx = data.find(kw)
    if idx > 0:
        chunk = data[idx:idx+400]
        text = re.sub(r'<[^>]+>', ' ', chunk)
        text = re.sub(r'\s+', ' ', text).strip()
        print(f'\n[{kw}@{idx}]:', text[:200])
