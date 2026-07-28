# -*- coding: utf-8 -*-
"""Retry the 2 failed pals and recompute distribution with various thresholds."""
import json, re, urllib.request, urllib.parse, time

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

# Load
rarity_data = json.load(open('scripts/paldb-rarity.json', encoding='utf-8'))
mapping = json.load(open('scripts/paldb-slug-mapping.json', encoding='utf-8'))
pals = json.load(open('src/data/pals.json', encoding='utf-8'))

# Retry failed
for palid in ['lifmunk', 'fuack']:
    pal = next(p for p in pals if p['id'] == palid)
    slug = mapping.get(palid) or pal['name']['en']
    for attempt in range(3):
        try:
            url = f'https://paldb.cc/en/{urllib.parse.quote(slug)}'
            req = urllib.request.Request(url, headers=HEADERS)
            r = urllib.request.urlopen(req, timeout=15)
            d = r.read().decode('utf-8', errors='ignore')
            m = re.search(r'<div>Rarity</div>.*?<div>(\d+)</div>', d, re.DOTALL)
            if m:
                rarity_data[palid] = int(m.group(1))
                print(f'  {palid}: R{int(m.group(1))}')
                break
        except Exception as e:
            print(f'  {palid} attempt {attempt+1}: {e}')
            time.sleep(2)

# Save updated
with open('scripts/paldb-rarity.json', 'w', encoding='utf-8') as f:
    json.dump(rarity_data, f, ensure_ascii=False, indent=2)

# Test multiple threshold schemes
from collections import Counter
cnt = Counter(rarity_data.values())
print('\n=== Threshold candidates ===')
print('Distribution:')
for r in sorted(cnt.keys()):
    print(f'  R{r}: {cnt[r]}')

print('\n--- Scheme A: 1-4 C / 5-8 R / 9-19 E / 20 L ---')
def sh_a(r):
    if r >= 20: return 'Legendary'
    if r >= 9: return 'Epic'
    if r >= 5: return 'Rare'
    return 'Common'
sa = Counter(sh_a(r) for r in rarity_data.values())
print(f'  {dict(sa)}')

print('--- Scheme B: 1-3 C / 4-7 R / 8-19 E / 20 L ---')
def sh_b(r):
    if r >= 20: return 'Legendary'
    if r >= 8: return 'Epic'
    if r >= 4: return 'Rare'
    return 'Common'
sb = Counter(sh_b(r) for r in rarity_data.values())
print(f'  {dict(sb)}')

print('--- Scheme C: 1-4 C / 5-7 R / 8-19 E / 20 L ---')
def sh_c(r):
    if r >= 20: return 'Legendary'
    if r >= 8: return 'Epic'
    if r >= 5: return 'Rare'
    return 'Common'
sc = Counter(sh_c(r) for r in rarity_data.values())
print(f'  {dict(sc)}')

print('--- Grok target: Common 120-140 / Rare 80-100 / Epic 40-60 / Leg 8-15 ---')
