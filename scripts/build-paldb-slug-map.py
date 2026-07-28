# -*- coding: utf-8 -*-
"""Build slug → paldb.cc URL mapping for all 288 pals.
Tries multiple slug variants until one works.
"""
import json, re, urllib.request, urllib.parse, time

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

# Load pals
pals = json.load(open('src/data/pals.json', encoding='utf-8'))

def make_slug_variants(en):
    """Generate possible paldb.cc URL slugs for a pal name."""
    en = en.strip()
    variants = []
    # 1. As-is
    variants.append(en)
    # 2. Spaces → underscores
    variants.append(en.replace(' ', '_'))
    # 3. Remove parentheses content
    clean = re.sub(r'\s*\([^)]+\)', '', en).strip()
    if clean != en:
        variants.append(clean)
        variants.append(clean.replace(' ', '_'))
    # 4. Special chars stripped
    no_special = re.sub(r"['\u2019]", '', en)
    if no_special != en:
        variants.append(no_special)
        variants.append(no_special.replace(' ', '_'))
    return list(dict.fromkeys(variants))  # dedupe preserving order

# Test a few to see what works
print('--- Test slug variants ---')
TEST = ['Mau Cryst', 'Foxparks Cryst', 'Celaray Lux', 'Gumoss (Special)', 'Cattiva', 'Panthalus', 'Neptilius', 'Bellanoir', 'Bellanoir Libero']
for en in TEST:
    variants = make_slug_variants(en)
    print(f'{en:30s} -> {variants[:3]}')

# Build full mapping by checking each pal
print(f'\n--- Building mapping for {len(pals)} pals ---')
mapping = {}
unmapped = []
checked = 0
for pal in pals:
    en = pal['name']['en']
    palid = pal['id']
    if palid in mapping:
        continue
    variants = make_slug_variants(en)
    found = False
    for v in variants:
        url = f'https://paldb.cc/en/{urllib.parse.quote(v)}'
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            r = urllib.request.urlopen(req, timeout=10)
            d = r.read().decode('utf-8', errors='ignore')
            if 'Rarity' in d and len(d) > 5000:  # valid pal page
                mapping[palid] = v
                found = True
                break
        except urllib.error.HTTPError as e:
            if e.code == 404:
                continue
        except Exception:
            continue
    checked += 1
    if not found:
        unmapped.append(palid)
    if checked % 30 == 0:
        print(f'  [{checked}/{len(pals)}] mapped={len(mapping)} unmapped={len(unmapped)}', flush=True)
    time.sleep(0.25)

print(f'\nTotal: {len(pals)}, Mapped: {len(mapping)}, Unmapped: {len(unmapped)}')
print('\nUnmapped pals:')
for palid in unmapped:
    pal = next(p for p in pals if p['id'] == palid)
    print(f'  {palid:30s} {pal["name"]["en"]:30s} ({pal["name"]["zh"]})')

# Save mapping
with open('scripts/paldb-slug-mapping.json', 'w', encoding='utf-8') as f:
    json.dump(mapping, f, ensure_ascii=False, indent=2)
print(f'\nSaved scripts/paldb-slug-mapping.json')
