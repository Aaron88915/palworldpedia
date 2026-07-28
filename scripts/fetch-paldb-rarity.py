# -*- coding: utf-8 -*-
"""Fetch rarity (1-20) for all 288 pals from paldb.cc."""
import json, re, urllib.request, urllib.parse, time

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

# Load pals + mapping
pals = json.load(open('src/data/pals.json', encoding='utf-8'))
mapping = json.load(open('scripts/paldb-slug-mapping.json', encoding='utf-8'))

# Manual overrides
mapping['green-slime'] = 'Green_Slime'
mapping['celaray-lux'] = 'Celaray_Lux'

print(f'Fetching rarity for {len(pals)} pals...')
rarity_data = {}
failed = []
for i, pal in enumerate(pals):
    palid = pal['id']
    slug = mapping.get(palid)
    if not slug:
        failed.append((palid, 'no-slug'))
        continue
    url = f'https://paldb.cc/en/{urllib.parse.quote(slug)}'
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        r = urllib.request.urlopen(req, timeout=15)
        d = r.read().decode('utf-8', errors='ignore')
        # Match the Rarity number after the Rarity label and progress bar
        m = re.search(r'<div>Rarity</div>.*?<div>(\d+)</div>', d, re.DOTALL)
        if m:
            rarity_data[palid] = int(m.group(1))
        else:
            failed.append((palid, f'no-rarity-match (slug={slug}, len={len(d)})'))
    except Exception as e:
        failed.append((palid, f'ERR {e}'))
    if (i + 1) % 30 == 0:
        print(f'  [{i+1}/{len(pals)}] got={len(rarity_data)} fail={len(failed)}', flush=True)
    time.sleep(0.3)

print(f'\n=== Results ===')
print(f'Total: {len(pals)}')
print(f'Got: {len(rarity_data)}')
print(f'Failed: {len(failed)}')
for palid, reason in failed:
    pal = next(p for p in pals if p['id'] == palid)
    print(f'  {palid:30s} {pal["name"]["en"]:30s} - {reason}')

# Save rarity data
with open('scripts/paldb-rarity.json', 'w', encoding='utf-8') as f:
    json.dump(rarity_data, f, ensure_ascii=False, indent=2)
print(f'\nSaved scripts/paldb-rarity.json')

# Distribution
from collections import Counter
print('\n--- Rarity distribution (1-20) ---')
cnt = Counter(rarity_data.values())
for r in sorted(cnt.keys()):
    print(f'  Rarity {r:2d}: {cnt[r]}')
