# -*- coding: utf-8 -*-
"""Download palworld.gg JS bundles and search for pal data with image URLs."""
import urllib.request, re, os, json

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

os.makedirs('scripts/palworldgg-bundles', exist_ok=True)

# Download all bundles
bundles = ['DD_femJf.js', 'Sm5RjUkj.js', 'BMkE8gdE.js', 'B9mNKYjW.js', 'aiJfK3Dn.js',
           'Dz-gzVwH.js', 'CpWWtyX8.js', 'DxLDlgif.js', 'BrmMxTD0.js', 'DJawUlvd.js',
           'D613kDhC.js', 'C3K0Onqi.js', 'ST5j10Sm.js', 'BHTn-jI_.js']
for b in bundles:
    if os.path.exists(f'scripts/palworldgg-bundles/{b}'):
        continue
    try:
        req = urllib.request.Request(f'https://palworld.gg/_nuxt/{b}', headers=HEADERS)
        d = urllib.request.urlopen(req, timeout=20).read().decode('utf-8', errors='ignore')
        with open(f'scripts/palworldgg-bundles/{b}', 'w', encoding='utf-8') as f:
            f.write(d)
        print(f'  {b}: {len(d)}')
    except Exception as e:
        print(f'  {b}: ERR {e}')

# Search for pal data patterns
all_bundles = sorted(os.listdir('scripts/palworldgg-bundles'))
for b in all_bundles:
    fpath = f'scripts/palworldgg-bundles/{b}'
    if not b.endswith('.js'):
        continue
    with open(fpath, encoding='utf-8') as f:
        d = f.read()
    # Look for image URL patterns (cloudfront/cloudinary)
    for kw in ['cloudfront.net', 'cloudinary', 'image/pals', '/pals/', 'image.palworld']:
        cnt = d.count(kw)
        if cnt > 0:
            # Find a sample URL
            idx = d.find(kw)
            ctx = d[max(0,idx-50):idx+250]
            print(f'  {b}: {kw} x{cnt}: {ctx[:200]}')
            break
