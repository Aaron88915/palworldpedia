# -*- coding: utf-8 -*-
"""Probe palworld.gg for image URLs of missing pals."""
import urllib.request, re, json, time

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html',
}

missing = [
    'green-slime', 'gumoss-special', 'fuack', 'celaray-lux', 'pupperai',
    'clovee', 'tanzee', 'rooby', 'foxparks-cryst', 'caprity-noct',
    'sparkit', 'loupmoon-cryst', 'fenglope-lux', 'dazzi-noct', 'dumud-gild',
    'kitsun-noct', 'warsect-terra', 'cryolinx-terra', 'whalaska-ignis', 'panthalus',
]

# palworld.gg URL pattern: /pals/{slug}
# slugs may differ from ours. Try common variants.
SLUG_VARIANTS = lambda name: [
    name, name.replace('-', ''), name.replace('-', ' '),
    name.replace('-', ' ').title(), name.replace('-', ' ').title().replace(' ', ''),
    name.title().replace('-', ''), name.title().replace('-', ' '),
    name.upper(), name.lower(),
]

for pal_id in missing[:5]:
    # Try URL
    for slug in [pal_id, pal_id.replace('-', ''), pal_id.replace('-', ' '), pal_id.replace('-', ' ').title()]:
        try:
            url = f'https://palworld.gg/pals/{urllib.parse.quote(slug)}'
            req = urllib.request.Request(url, headers=HEADERS)
            r = urllib.request.urlopen(req, timeout=15)
            d = r.read().decode('utf-8', errors='ignore')
            # Find image
            imgs = re.findall(r'<img[^>]+src="([^"]+)"', d)
            pal_imgs = [u for u in imgs if 'pal' in u.lower() or 'thumb' in u.lower() or 'icon' in u.lower()]
            if pal_imgs:
                print(f'\n=== {pal_id} (slug={slug}) ===')
                for img in pal_imgs[:5]:
                    print(f'  {img[:200]}')
                break
        except urllib.error.HTTPError as e:
            if e.code == 404:
                continue
        except Exception as e:
            print(f'  {pal_id}/{slug}: ERR {e}')
    time.sleep(0.3)
