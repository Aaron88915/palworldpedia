# -*- coding: utf-8 -*-
"""Download missing pal images from palworld.gg using their texture names."""
import urllib.request, re, json, time, os

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

# Load our pals
pals = json.load(open('src/data/pals.json', encoding='utf-8'))

# Load palworld.gg pal data
with open('scripts/palworldgg-bundles/CK2A4_hG.js', encoding='utf-8') as f:
    bundle = f.read()

# Build slug -> icon name map by parsing the bundle
# Pattern: {id:"...", slug:"fuack", name:"Fuack", ..., icon:"T_BluePlatypus_icon_normal", ...}
# Use a regex to extract {id, slug, name, icon}
gg_pals = []
for m in re.finditer(r'\{id:"([^"]+)",[^}]*?slug:"([^"]+)",[^}]*?name:"([^"]+)",[^}]*?icon:"([^"]+)"', bundle):
    gg_pals.append({'id': m.group(1), 'slug': m.group(2), 'name': m.group(3), 'icon': m.group(4)})
print(f'palworld.gg pals parsed: {len(gg_pals)}')
print('First 3:', gg_pals[:3])

# Build map: our pal id -> gg icon name
# Match by English name (case-insensitive)
our_by_en = {p['name']['en'].lower().strip(): p['id'] for p in pals}
gg_by_en = {p['name'].lower().strip(): p for p in gg_pals}

# Find missing pals
img_dir = 'public/images/pals'
missing = []
for p in pals:
    img_path = p.get('image', '')
    if not img_path:
        missing.append(p)
        continue
    fname = os.path.basename(img_path)
    fpath = os.path.join(img_dir, fname)
    if not os.path.exists(fpath):
        missing.append(p)

print(f'\nMissing images: {len(missing)}')

# For each missing, find gg pal by English name
fetched = 0
not_found = []
for p in missing:
    en = p['name']['en'].lower().strip()
    gg = gg_by_en.get(en)
    if not gg:
        not_found.append((p['id'], p['name']['en'], p['name']['zh']))
        continue
    icon = gg['icon']
    # Try several URL patterns
    url_options = [
        f'https://palworld.gg/images/full_palicon/{icon}.png',
        f'https://palworld.gg/images/pal_icon/{icon}.png',
        f'https://palworld.gg/images/pals/{icon}.png',
    ]
    for url in url_options:
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            r = urllib.request.urlopen(req, timeout=20)
            data = r.read()
            if len(data) < 100:
                continue
            # Save
            fname = os.path.basename(p.get('image', ''))
            if not fname:
                fname = f"{gg['slug']}.png"
            save_path = os.path.join(img_dir, fname)
            with open(save_path, 'wb') as f:
                f.write(data)
            print(f'  ✓ {p["id"]:30s} -> {fname} ({len(data)} bytes) <- {url}')
            fetched += 1
            break
        except Exception as e:
            continue
    time.sleep(0.3)

print(f'\nFetched: {fetched}/{len(missing)}')
if not_found:
    print(f'\nNot found on palworld.gg:')
    for pid, en, zh in not_found:
        print(f'  {pid:30s} {en:30s} ({zh})')
