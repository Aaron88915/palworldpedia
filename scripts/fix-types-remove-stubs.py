#!/usr/bin/env python3
"""
Fix element types for the 16 enriched pals (from known game data).
Remove 8 truly-missing stubs (Boltmane etc.) that have no data anywhere.
Keep the 9 properly-enriched pals.
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
PALS_JSON = ROOT / 'src' / 'data' / 'pals.json'

# Correct element types based on palcalc InternalName + game knowledge
TYPE_FIX = {
    'fuack':         ['water'],
    'clovee':        ['grass'],
    'tanzee':        ['grass'],
    'rooby':         ['fire'],
    'pupperai':      ['dark'],
    'sparkit':       ['electric'],
    'foxparks-cryst': ['ice'],
    'celaray-lux':   ['electric'],
    'caprity-noct':  ['dark'],
    'loupmoon-cryst': ['ice'],
    'fenglope-lux':  ['electric'],
    'dazzi-noct':    ['water'],
    'dumud-gild':    ['dragon'],
    'kitsun-noct':   ['dark'],
    'cryolinx-terra': ['ground'],
    'gumoss-special': ['grass', 'ground'],
    'ribbuny':       ['normal'],  # was 'neutral', palcalc says 'normal'
}

# 8 pals with no data anywhere — remove
TO_REMOVE = ['boltmane', 'cyan-wolf-cub', 'dark-mutant', 'dragostrophe',
             'feathered-dragon', 'astralym', 'ribunny']

pals = json.load(open(PALS_JSON, 'r', encoding='utf-8'))
print(f'Before: {len(pals)} pals')

# Apply type fixes
for p in pals:
    if p['id'] in TYPE_FIX:
        old = p['types']
        p['types'] = TYPE_FIX[p['id']]
        if old != TYPE_FIX[p['id']]:
            print(f'  type fix: {p["id"]} {old} -> {TYPE_FIX[p["id"]]}')

# Remove stubs
removed = []
pals = [p for p in pals if p['id'] not in TO_REMOVE]
removed_count = len(TO_REMOVE)
for pid in TO_REMOVE:
    removed.append(pid)

print(f'\nRemoved {removed_count} stubs: {removed}')
print(f'After: {len(pals)} pals')

# Re-sort
def sort_key(p):
    en = p['name']['en']
    has_space = ' ' in en
    return (p['paldeckNo'], has_space, p['name']['en'])

pals.sort(key=sort_key)

# Save
with open(PALS_JSON, 'w', encoding='utf-8') as f:
    json.dump(pals, f, ensure_ascii=False, indent=2)

print(f'\nSaved {PALS_JSON}')

# Regenerate compact pals-data.json
PALS_DATA = ROOT / 'public' / 'pals-data.json'
compact = [
    {
        'id': p['id'],
        'zh': p['name']['zh'],
        'en': p['name']['en'],
        'types': p['types'],
        'img': p['image'],
    }
    for p in pals
]
with open(PALS_DATA, 'w', encoding='utf-8') as f:
    json.dump(compact, f, ensure_ascii=False, separators=(',', ':'))
print(f'Rewrote {PALS_DATA}')

# Also check breeding-data.json indices - we removed 8 pals, so indices shifted!
# We need to rebuild breeding-data.json too
BREED_DATA = ROOT / 'public' / 'breeding-data.json'
print(f'\nNOTE: breeding-data.json needs rebuild (indices shifted after removing 8 pals)')
