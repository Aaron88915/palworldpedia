# -*- coding: utf-8 -*-
"""Map palcalc InternalNames to Fandom wiki page titles."""
import json

# Load palcalc
db = json.load(open('scripts/raw-palcalc-db.json', encoding='utf-8'))
pals = db['Pals']

# Load fandom titles
titles = json.load(open('scripts/fandom-all-titles.json', encoding='utf-8'))
title_set = set(titles)

# Build mapping: InternalName -> candidate Fandom titles
# For non-variant: pal.Name (e.g., "Lamball")
# For variant: pal.Name + " (suffix)" pattern OR pal.Name + " " + suffix word
# We need the suffix list

# Build a base pal lookup (non-variant)
base_pal_name = {}  # English name -> InternalName
for p in pals:
    if not p['Id']['IsVariant']:
        base_pal_name[p['Name']] = p['InternalName']

print(f'Base pals: {len(base_pal_name)}')

# Known suffix map (InternalName suffix -> human word)
SUFFIX_MAP = {
    '_Dark': 'Noct',
    '_Ice': 'Cryst',
    '_Fire': 'Ignis',
    '_Electric': 'Lux',
    '_Grass': 'Botan',
    '_Ground': 'Terra',
    '_Dragon': 'Gild',
    '_Water': 'Hydro',
    '_Blaze': 'Blaze',
    '_Astral': 'Astral',
    '_Noct': 'Noct',
    '_Botan': 'Botan',
    '_Ignis': 'Ignis',
    '_Cryst': 'Cryst',
    '_Lux': 'Lux',
    '_Terra': 'Terra',
    '_Hydro': 'Hydro',
    '_Gild': 'Gild',
    '_Special': 'Special',
    '_Jelly': 'Jelly',
    '_Stream': 'Stream',
    '_Alpine': 'Alpine',
    '_Forest': 'Forest',
    '_Obsidian': 'Obsidian',
    '_Crystal': 'Crystal',
    '_Fantasm': 'Fantasm',
    '_Storm': 'Storm',
    '_Shadow': 'Shadow',
    '_Stone': 'Stone',
    '_King': 'King',
    '_Royal': 'Royal',
    '_Air': 'Air',
    '_Emperor': 'Emperor',
    '_Observer': 'Observer',
    '_Lovely': 'Lovely',
    '_Crusher': 'Crusher',
    '_Blockhead': 'Blockhead',
    '_Libero': 'Libero',
    '_Umbral': 'Umbral',
    '_Master': 'Master',
}

# Try multiple naming patterns for each pal
mapping = {}  # InternalName -> Fandom title
unmapped = []

for p in pals:
    name = p['Name']
    iname = p['InternalName']
    is_variant = p['Id']['IsVariant']

    # Try direct match
    if name in title_set:
        mapping[iname] = name
        continue

    # For variants: try "Name Suffix" where Suffix is mapped
    if is_variant:
        # Find suffix in InternalName
        for key, suffix in SUFFIX_MAP.items():
            if iname.endswith(key):
                base = iname[:-len(key)]
                base_pal = next((pp for pp in pals if pp['InternalName'] == base), None)
                if base_pal:
                    base_name = base_pal['Name']
                    candidate = f'{base_name} {suffix}'
                    if candidate in title_set:
                        mapping[iname] = candidate
                        break
        else:
            unmapped.append(iname)
    else:
        unmapped.append(iname)

print(f'\nMapped: {len(mapping)}/{len(pals)}')
print(f'Unmapped: {len(unmapped)}')
for u in unmapped[:50]:
    print(f'  {u}')

# Save
json.dump(mapping, open('scripts/pal-fandom-mapping.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print(f'\nSaved to scripts/pal-fandom-mapping.json')
