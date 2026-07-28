# -*- coding: utf-8 -*-
"""Build slug-based Fandom mapping. pals.json uses lowercase slugs (e.g., 'green-slime')."""
import json

db = json.load(open('scripts/raw-palcalc-db.json', encoding='utf-8'))
pals = db['Pals']

# Load slug mapping from pals.json
our_pals = json.load(open('src/data/pals.json', encoding='utf-8'))
our_by_slug = {p['id']: p for p in our_pals}

# Build slug->InternalName map
# pals.json slugs: lowercase, hyphenated (e.g., 'gumoss-special', 'foxparks-cryst')
# palcalc InternalName: PascalCase with underscore (e.g., 'Gumoss_Special', 'Foxparks_Cryst')
def to_internal(slug):
    """Convert 'gumoss-special' to 'Gumoss_Special'."""
    parts = slug.split('-')
    return '_'.join(p.capitalize() for p in parts)

# Load fandom title set
titles = json.load(open('scripts/fandom-all-titles.json', encoding='utf-8'))
title_set = set(titles)

# Load existing mapping (InternalName -> Fandom title)
existing = json.load(open('scripts/pal-fandom-mapping.json', encoding='utf-8'))

# Now build slug -> Fandom title mapping
slug_to_fandom = {}
unmapped = []

for slug, pal in our_by_slug.items():
    iname = to_internal(slug)
    title = existing.get(iname)
    if title:
        slug_to_fandom[slug] = title
    else:
        unmapped.append((slug, iname, pal.get('en', '?')))

print(f'Mapped: {len(slug_to_fandom)}/{len(our_by_slug)}')
print(f'Unmapped: {len(unmapped)}')
for s, i, en in unmapped[:30]:
    print(f'  {s:30s} ({i}, en={en})')

json.dump(slug_to_fandom, open('scripts/slug-to-fandom.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('Saved scripts/slug-to-fandom.json')
