import urllib.request, re
UA = {'User-Agent': 'Mozilla/5.0'}

# Try alt names for some popular ones
candidates = [
    # Palbox
    ('T_icon_buildObject_PalBoxV2.webp', 'Palbox'),
    # Pal Sphere - check different grade names
    ('T_itemicon_Special_PalSphere_Grade_01.webp', 'Pal Sphere'),
    ('T_itemicon_Special_PalSphere_Grade_02.webp', 'Mega Sphere'),
    ('T_itemicon_Special_PalSphere_Grade_03.webp', 'Giga Sphere'),
    # Build objects alt names
    ('T_icon_buildObject_PalBox.webp', 'Palbox alt'),
    ('T_icon_buildObject_PalStorage.webp', 'Palbox alt2'),
    ('T_icon_buildObject_PalboxV1.webp', 'Palbox alt3'),
    ('T_icon_buildObject_Palbox_v2.webp', 'Palbox alt4'),
]
base1 = 'https://cdn.paldb.cc/image/Pal/Texture/BuildObject/PNG/'
base2 = 'https://cdn.paldb.cc/image/Others/InventoryItemIcon/Texture/'

for fname, label in candidates:
    for base in [base1, base2]:
        url = base + fname
        try:
            req = urllib.request.Request(url, headers=UA)
            r = urllib.request.urlopen(req, timeout=10)
            body = r.read()
            print(f'OK {r.status} {len(body):>5}B  {label}: {url}')
        except Exception as e:
            pass  # skip

# Also check what URLs are in the existing paldb.cc technologies page HTML
print()
print('=== From saved paldb-technologies.html ===')
import os
if os.path.exists('scripts/paldb-technologies.html'):
    with open('scripts/paldb-technologies.html', 'r', encoding='utf-8') as f:
        h = f.read()
    # Find buildObject_PalBox or similar
    for kw in ['PalBox', 'Palbox', 'PalSphere', 'GlobalPalStorage']:
        for m in re.finditer(re.escape(kw), h, re.IGNORECASE):
            idx = m.start()
            ctx = re.sub(r'\s+', ' ', h[max(0,idx-100):idx+200])
            print(f'{kw} @ {idx}: {ctx[:300]}')
            break
