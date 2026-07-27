#!/usr/bin/env python3
"""
Update pals.json with proper Chinese names from palcalc db.json
and fix element types based on palcalc InternalName analysis.
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
PALS_JSON = ROOT / 'src' / 'data' / 'pals.json'
PALCALC_DB = ROOT / 'scripts' / 'raw-palcalc-db.json'

# Manual type corrections based on palcalc InternalName analysis:
# - InternalName typically encodes the type (e.g., BluePlatypus is Water, Hedgehog_Ice is Ice)
# - Variants have _Ice, _Dark, _Ground, _Fire, _Electric, _Water, _Dragon, _Leaf, _Gold suffixes
# Mapping for the 17 missing pals:
TYPE_FIX = {
    'clovee': ['grass'],          # CloverFairy = grass
    'dazzi-noct': ['water'],      # RaijinDaughter_Water
    'dumud-gild': ['dragon'],     # LazyCatfish_Gold - special, but dragon works
    'celaray-lux': ['electric'],  # FlyingManta_Thunder
    'fenglope-lux': ['electric'], # FengyunDeeper_Electric
    'sparkit': ['electric'],      # ElecCat
    'pupperai': ['dark'],         # SamuraiDog
}

# Chinese names from palcalc
ZH_NAMES = {
    'fuack':         '冲浪鸭',
    'clovee':        '幸叶茸',
    'tanzee':        '新叶猿',
    'rooby':         '燎火鹿',
    'pupperai':      '宗铭丸',
    'sparkit':       '伏特喵',
    'ribunny':       '兔兔',
    'foxparks-cryst':'雪绒狐',
    'celaray-lux':   '雷米儿',
    'caprity-noct':  '郁木羊',
    'loupmoon-cryst':'霜镰魔',
    'fenglope-lux':  '雷隐鹿',
    'dazzi-noct':    '天阴童子',
    'dumud-gild':    '梆梆鲶',
    'kitsun-noct':   '幽焰狼',
    'cryolinx-terra':'金棘兽',
    'gumoss-special':'叶泥泥',
}

with open(PALS_JSON, 'r', encoding='utf-8') as f:
    pals = json.load(f)

# Build id -> entry map
m = {p['id']: p for p in pals}

updated = []
for pid, zh in ZH_NAMES.items():
    if pid not in m:
        print(f'  ! {pid} not in DB, skipping')
        continue
    p = m[pid]
    old_zh = p['name']['zh']
    p['name']['zh'] = zh
    if pid in TYPE_FIX:
        old_types = p['types']
        p['types'] = TYPE_FIX[pid]
        print(f'  {pid}: zh={old_zh!r} -> {zh!r}, types={old_types} -> {TYPE_FIX[pid]}')
    else:
        print(f'  {pid}: zh={old_zh!r} -> {zh!r}')
    updated.append(pid)

# Save
with open(PALS_JSON, 'w', encoding='utf-8') as f:
    json.dump(pals, f, ensure_ascii=False, indent=2)

print(f'\nUpdated {len(updated)} pals. Saved {PALS_JSON}')

# Also regenerate compact pals-data.json
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

# Print summary
print('\n--- Updated pals summary ---')
for pid in updated:
    p = m[pid]
    print(f"  {p['id']:25s} {p['name']['zh']:10s} / {p['name']['en']:25s} types={p['types']}")
