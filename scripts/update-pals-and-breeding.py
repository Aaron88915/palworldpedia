#!/usr/bin/env python3
"""
Update pals.json with 17 missing pals from beckerfelipee 1.0 dataset,
then regenerate breeding edges in COMPACT INDEX format.

Compact format: each edge is [idx1, idx2, child_idx] with idx1 <= idx2.
Pal indices come from the array position in pals-data.json.
"""
import json
import os
from pathlib import Path

ROOT = Path(__file__).parent.parent
RAW_DIR = ROOT / 'scripts'
PALS_JSON = ROOT / 'src' / 'data' / 'pals.json'
OUT_DATA = ROOT / 'public' / 'pals-data.json'  # compact pals (for breeding page)
OUT_BREED = ROOT / 'public' / 'breeding-data.json'  # compact edges

# ------------------------------------------------------------------
# Step 1: Add missing pals
# ------------------------------------------------------------------

# Format: (id, en_name, zh_name, types, paldeckNo, image_filename)
# zh_name uses en_name as fallback - we'll translate properly later
# Types inferred from naming patterns + palcalc db.json knowledge
MISSING_PALS = [
    # 7 base pals not in our DB
    ('fuack',     'Fuack',     'Fuack',     ['water'],        10, 'Fuack.png'),
    ('clovee',    'Clovee',    'Clovee',    ['normal'],        0, 'Clovee.png'),
    ('tanzee',    'Tanzee',    'Tanzee',    ['grass'],         0, 'Tanzee.png'),
    ('rooby',     'Rooby',     'Rooby',     ['fire'],          0, 'Rooby.png'),
    ('pupperai',  'Pupperai',  'Pupperai',  ['dark'],          0, 'Pupperai.png'),
    ('sparkit',   'Sparkit',   'Sparkit',   ['electric'],      0, 'Sparkit.png'),
    ('ribunny',   'Ribunny',   'Ribunny',   ['grass'],         0, 'Ribunny.png'),
    # 9 variants — type is variant suffix
    ('foxparks-cryst',  'Foxparks Cryst',  'Foxparks Cryst',  ['ice'],         29, 'Foxparks Cryst.png'),
    ('celaray-lux',     'Celaray Lux',     'Celaray Lux',     ['electric'],     7, 'Celaray Lux.png'),
    ('caprity-noct',    'Caprity Noct',    'Caprity Noct',    ['dark'],         0, 'Caprity Noct.png'),
    ('loupmoon-cryst',  'Loupmoon Cryst',  'Loupmoon Cryst',  ['ice'],          0, 'Loupmoon Cryst.png'),
    ('fenglope-lux',    'Fenglope Lux',    'Fenglope Lux',    ['electric'],     0, 'Fenglope Lux.png'),
    ('dazzi-noct',      'Dazzi Noct',      'Dazzi Noct',      ['dark'],         0, 'Dazzi Noct.png'),
    ('dumud-gild',      'Dumud Gild',      'Dumud Gild',      ['dragon'],       0, 'Dumud Gild.png'),
    ('kitsun-noct',     'Kitsun Noct',     'Kitsun Noct',     ['dark'],         0, 'Kitsun Noct.png'),
    ('cryolinx-terra',  'Cryolinx Terra',  'Cryolinx Terra',  ['ground'],       0, 'Cryolinx Terra.png'),
    # 1 special - gumoss flower variant
    ('gumoss-special',  'Gumoss (Special)', 'Gumoss (Special)', ['grass', 'ground'], 0, 'Gumoss (Special).png'),
]

def make_pal_entry(pal_id, en_name, zh_name, types, paldeck_no, image):
    return {
        'id': pal_id,
        'paldeckNo': paldeck_no,
        'name': {'zh': zh_name, 'en': en_name},
        'types': types,
        'rarity': 1,
        'stats': {
            'hp': 0,
            'attack': {'melee': 0, 'ranged': 0},
            'defense': 0,
            'speed': 0,
        },
        'workSuitability': {},
        'skills': [],
        'passives': [],
        'drops': [],
        'food': 0,
        'price': 0,
        'biomes': [],
        'nightOnly': False,
        'description': {'zh': '', 'en': ''},
        'image': f'/images/pals/{image}',
        'breedpower': 0,
        'updatedAt': '2026-07-28',
    }

with open(PALS_JSON, 'r', encoding='utf-8') as f:
    pals = json.load(f)

# Build existing id set
existing_ids = {p['id'] for p in pals}
print(f'Existing pals: {len(pals)}')

# Track which to add
to_add = []
for pal in MISSING_PALS:
    if pal[0] not in existing_ids:
        to_add.append(pal)
    else:
        print(f'  Skipping (exists): {pal[0]}')

print(f'\nAdding {len(to_add)} new pals:')
for pal in to_add:
    print(f'  + {pal[0]:25s} {pal[1]:25s} {pal[3]}')
    pals.append(make_pal_entry(*pal))

# Reorder: base pals first, then variants
def sort_key(p):
    en = p['name']['en']
    has_space = ' ' in en
    return (p['paldeckNo'], has_space, p['name']['en'])

pals.sort(key=sort_key)

# Save
with open(PALS_JSON, 'w', encoding='utf-8') as f:
    json.dump(pals, f, ensure_ascii=False, indent=2)

print(f'\nSaved {PALS_JSON} with {len(pals)} pals')

# ------------------------------------------------------------------
# Step 2: Generate compact pals-data.json (id, name.zh, name.en, types, image)
# ------------------------------------------------------------------
compact_pals = [
    {
        'id': p['id'],
        'zh': p['name']['zh'],
        'en': p['name']['en'],
        'types': p['types'],
        'img': p['image'],
    }
    for p in pals
]
with open(OUT_DATA, 'w', encoding='utf-8') as f:
    json.dump(compact_pals, f, ensure_ascii=False, separators=(',', ':'))
print(f'Wrote {OUT_DATA} ({os.path.getsize(OUT_DATA)/1024:.1f} KB)')

# ------------------------------------------------------------------
# Step 3: Build compact breeding edges from becker AllCombos
# ------------------------------------------------------------------
# Build name (en) -> index
name_to_idx = {}
for i, p in enumerate(compact_pals):
    name_to_idx[p['en'].lower()] = i
    name_to_idx[p['id'].lower()] = i  # also by id

# Load becker roster + matrix
with open(RAW_DIR / 'raw-beckerfelipee-Pals.csv', 'r', encoding='utf-8-sig') as f:
    roster = [line.strip() for line in f if line.strip()]

import csv
with open(RAW_DIR / 'raw-beckerfelipee-AllCombos.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.reader(f, delimiter=';')
    matrix = list(reader)

print(f'\nBecker matrix: {len(matrix)}×{len(roster)}')

# Map: for each (row, col), find child index
edges = []
unmapped_count = 0
for row in range(len(roster)):
    if len(matrix[row]) != len(roster):
        continue
    p1_name = roster[row]
    p1_idx = name_to_idx.get(p1_name.lower())
    if p1_idx is None:
        unmapped_count += 1
        continue
    for col in range(row, len(roster)):  # upper triangle only
        p2_name = roster[col]
        p2_idx = name_to_idx.get(p2_name.lower())
        child_name = matrix[row][col]
        child_idx = name_to_idx.get(child_name.lower())
        if p2_idx is None or child_idx is None:
            unmapped_count += 1
            continue
        # Sort parents for dedup
        a, b = sorted([p1_idx, p2_idx])
        edges.append([a, b, child_idx])

# Dedupe
unique_edges = list({tuple(e): e for e in edges}.values())
unique_edges.sort()
print(f'\nTotal edges (compact): {len(unique_edges)}')
print(f'Unmapped cells: {unmapped_count}')

# Save as compact JSON
with open(OUT_BREED, 'w', encoding='utf-8') as f:
    json.dump(unique_edges, f, ensure_ascii=False, separators=(',', ':'))
print(f'Wrote {OUT_BREED} ({os.path.getsize(OUT_BREED)/1024:.1f} KB)')

# ------------------------------------------------------------------
# Step 4: Verify with tests
# ------------------------------------------------------------------
def lookup(idx):
    return compact_pals[idx]['en']

def find(p1_name, p2_name):
    p1_idx = name_to_idx.get(p1_name.lower())
    p2_idx = name_to_idx.get(p2_name.lower())
    if p1_idx is None or p2_idx is None:
        return None
    a, b = sorted([p1_idx, p2_idx])
    for e in unique_edges:
        if e[0] == a and e[1] == b:
            return lookup(e[2])
    return None

print('\n--- Verification Tests ---')
tests = [
    ('Celaray', 'Lifmunk', 'should be Rushoar (was missing in wiki data)'),
    ('Lamball', 'Lamball', 'self-breed'),
    ('Katress', 'Wixen', 'gender-dependent, should be Katress Ignis'),
    ('Lamball', 'Cattiva', 'should be Daedream'),
    ('Foxparks', 'Foxparks Cryst', 'base + variant'),
    ('Gumoss', 'Gumoss (Special)', 'gumoss special'),
    ('Anubis', 'Anubis', 'self-breed rare'),
    ('Jormuntide', 'Jormuntide', 'self-breed rare'),
]
for p1, p2, note in tests:
    result = find(p1, p2)
    print(f'  {p1:25s} + {p2:25s} = {result}  ({note})')
