# -*- coding: utf-8 -*-
"""Find which bundle has actual pal data with names."""
import os, re

bundle_dir = 'scripts/palworldgg-bundles'
pal_test_names = ['Lamball', 'Cattiva', 'Mau Cryst', 'Anubis', 'Cawgnito']

# All bundles we have
all_bundles = sorted([f for f in os.listdir(bundle_dir) if f.endswith('.js')])
print('Bundles:', all_bundles)

# Need to download more bundles - we may be missing some
# Let me also check what bundles are referenced from main HTML vs from other bundles

# Check all bundles for any of the pal names
for fname in all_bundles:
    fpath = os.path.join(bundle_dir, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        d = f.read()
    for name in pal_test_names:
        if name in d:
            idx = d.find(name)
            ctx = d[max(0,idx-200):idx+300]
            ctx = re.sub(r'\s+', ' ', ctx)
            print(f'\n=== {fname}: "{name}" @ {idx} ===')
            print(ctx)
            break
