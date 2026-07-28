# -*- coding: utf-8 -*-
"""Build slug -> Fandom title mapping for ALL 288 pals, then fetch biomes + drops for those missing them."""
import urllib.request, json, urllib.parse, time, re, sys

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json',
}

# Load existing data
pals = json.load(open('src/data/pals.json', encoding='utf-8'))
fandom_titles = json.load(open('scripts/fandom-all-titles.json', encoding='utf-8'))
title_set = set(fandom_titles)

# Known suffix -> human word (Fandom naming convention)
SUFFIX_MAP = {
    '_Dark': 'Noct', '_Ice': 'Cryst', '_Fire': 'Ignis',
    '_Electric': 'Lux', '_Grass': 'Botan', '_Ground': 'Terra',
    '_Dragon': 'Gild', '_Water': 'Hydro', '_Blaze': 'Blaze',
    '_Astral': 'Astral', '_Aqua': 'Aqua',
    # Our specific ones
    '_Special': 'Special', '_Jelly': 'Jelly', '_Stream': 'Stream',
    '_Alpine': 'Alpine', '_Forest': 'Forest', '_Obsidian': 'Obsidian',
    '_Crystal': 'Crystal', '_Fantasm': 'Fantasm', '_Storm': 'Storm',
    '_Shadow': 'Shadow', '_Stone': 'Stone', '_King': 'King',
    '_Royal': 'Royal', '_Air': 'Air', '_Emperor': 'Emperor',
    '_Observer': 'Observer', '_Lovely': 'Lovely', '_Crusher': 'Crusher',
    '_Blockhead': 'Blockhead', '_Libero': 'Libero', '_Umbral': 'Umbral',
    '_Master': 'Master', '_Ryu': 'Ryu', '_Primo': 'Primo',
    '_Terra': 'Terra', '_Cryst': 'Cryst', '_Ignis': 'Ignis',
    '_Lux': 'Lux', '_Noct': 'Noct', '_Botan': 'Botan',
    '_Gild': 'Gild', '_Hydro': 'Hydro',
    # Suffixes that are sometimes removed in wiki
    '_1': '', '_2': '', '_3': '',
}

# Convert slug -> PascalCase InternalName
def slug_to_internal(slug):
    parts = slug.split('-')
    return '_'.join(p.capitalize() for p in parts)

# Find Fandom title for slug
def find_title(slug):
    iname = slug_to_internal(slug)

    # Try variant with suffix
    for key, suffix in SUFFIX_MAP.items():
        if iname.endswith(key) and suffix:
            base = iname[:-len(key)]
            base_parts = re.findall(r'[A-Z][a-z]*', base)
            base_slug = '-'.join(s.lower() for s in base_parts)
            base_pal = next((p for p in pals if p['id'] == base_slug), None)
            if base_pal:
                base_en = base_pal['name']['en']
                candidate = f'{base_en} {suffix}'
                if candidate in title_set:
                    return candidate
            # If base_pal not in our list, still try
            base_en_words = re.findall(r'[A-Z][a-z]*', base)
            base_en = ' '.join(base_en_words)
            candidate = f'{base_en} {suffix}'
            if candidate in title_set:
                return candidate

    # Direct: try pal.name.en
    pal = next((p for p in pals if p['id'] == slug), None)
    if pal:
        en = pal['name']['en']
        if en in title_set:
            return en

    return None

# Test mapping
print('=== Testing slug -> Fandom title mapping ===')
unmapped = []
mapping = {}
for pal in pals:
    title = find_title(pal['id'])
    if title:
        mapping[pal['id']] = title
    else:
        unmapped.append(pal['id'])

print(f'Mapped: {len(mapping)}/{len(pals)}')
print(f'Unmapped: {len(unmapped)}')
for u in unmapped[:20]:
    print(f'  {u}')

json.dump(mapping, open('scripts/slug-to-fandom-final.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('Saved slug-to-fandom-final.json')
