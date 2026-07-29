# -*- coding: utf-8 -*-
"""Scan all bundles for breeding data and pal data."""
import os, re, json

# Look for unique pal names in each bundle
pal_names = ['Lamball', 'Cattiva', 'Mau', 'Lifmunk', 'Foxparks', 'Anubis']

bundle_dir = 'scripts/palworldgg-bundles'
for fname in sorted(os.listdir(bundle_dir)):
    fpath = os.path.join(bundle_dir, fname)
    size = os.path.getsize(fpath)
    with open(fpath, 'r', encoding='utf-8') as f:
        d = f.read()
    pals_found = [p for p in pal_names if p in d]
    # Look for breeding-related content
    has_breed = bool(re.search(r'\bbreed', d, re.IGNORECASE))
    has_rank = bool(re.search(r'rank|Rank', d))
    has_combo = bool(re.search(r'combination|Combination|combo|Combo', d))
    print(f'{fname} ({size}b): pals={pals_found}, breed={has_breed}, rank={has_rank}, combo={has_combo}')
    if pals_found or (has_breed and has_combo):
        # Show first relevant snippet
        for kw in ['breed', 'combination', 'combo', 'path']:
            for m in re.finditer(rf'\b{re.escape(kw)}', d, re.IGNORECASE):
                idx = m.start()
                ctx = d[max(0,idx-100):idx+200]
                ctx = re.sub(r'\s+', ' ', ctx)[:300]
                print(f'   [{kw}] ...{ctx}...')
                break
        print()
