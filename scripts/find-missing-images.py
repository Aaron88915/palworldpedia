# -*- coding: utf-8 -*-
"""Find pals without local images and prepare for fallback download from palworld.gg."""
import json, os, urllib.parse, re

pals = json.load(open('src/data/pals.json', encoding='utf-8'))
img_dir = 'public/images/pals'

missing = []
have = []
for p in pals:
    img_path = p.get('image', '')
    if not img_path:
        missing.append({'id': p['id'], 'en': p['name']['en'], 'zh': p['name']['zh'], 'image': img_path})
        continue
    # Convert URL path to local file
    fname = os.path.basename(img_path)
    fpath = os.path.join(img_dir, fname)
    if os.path.exists(fpath):
        have.append(p['id'])
    else:
        missing.append({'id': p['id'], 'en': p['name']['en'], 'zh': p['name']['zh'], 'image': img_path, 'expected_file': fname})

print(f'Total pals: {len(pals)}')
print(f'Have images: {len(have)}')
print(f'Missing: {len(missing)}')
print()
for m in missing:
    print(f'  {m["id"]:30s} {m["en"]:30s} ({m["zh"]}) -> {m.get("expected_file", "?")}')
