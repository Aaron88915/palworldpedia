# -*- coding: utf-8 -*-
import json, re

pals = json.load(open('src/data/pals.json', encoding='utf-8'))
need = [p for p in pals if not p.get('biomes')]

# Variant suffixes (lowercase, case-insensitive)
VARIANT_SUFFIXES = [
    'dark', 'ice', 'fire', 'electric', 'grass', 'ground', 'dragon',
    'water', 'blaze', 'astral', 'aqua', 'special', 'jelly',
    'stream', 'alpine', 'forest', 'obsidian', 'crystal', 'fantasm',
    'storm', 'shadow', 'stone', 'king', 'royal', 'air', 'emperor',
    'observer', 'lovely', 'crusher', 'blockhead', 'libero', 'umbral',
    'master', 'ryu', 'primo',
    'terra', 'cryst', 'ignis', 'lux', 'noct', 'botan', 'gild', 'hydro',
]

def is_variant(pid):
    for s in VARIANT_SUFFIXES:
        if pid.endswith('-' + s):
            return True, pid[:-(len(s) + 1)]
    return False, None

special_ids = {'green-slime', 'gumoss-special', 'neptilius', 'jetragon', 'panthalus'}

special = []
variants = []  # list of (pal, base_id)
bases = []

for p in need:
    pid = p['id']
    pno = p.get('paldeckNo', 0)
    is_var, base_id = is_variant(pid)
    if pno == 0 or pno >= 201 or pid in special_ids:
        special.append(p)
    elif is_var:
        variants.append((p, base_id))
    else:
        bases.append(p)

print('Special: %d' % len(special))
for p in special:
    print('  %s paldeckNo=%d types=%s' % (p['id'], p.get('paldeckNo', 0), p.get('types', [])))
print()

print('Variants: %d' % len(variants))
for p, bid in variants:
    print('  %-30s -> base=%s' % (p['id'], bid))
print()

print('Bases: %d' % len(bases))
for p in bases:
    print('  %-30s paldeckNo=%-3d types=%s' % (p['id'], p.get('paldeckNo', 0), p.get('types', [])))

# Check if variant's base has biomes
print()
print('=== variant base availability ===')
missing = []
for p, bid in variants:
    base_pal = next((x for x in pals if x['id'] == bid), None)
    if base_pal is None:
        missing.append(p['id'])
        print('  %-30s -> base %s NOT FOUND' % (p['id'], bid))
    else:
        print('  %-30s -> base %s biomes=%s' % (p['id'], bid, base_pal.get('biomes', [])))
print()
print('Variants without base:', len(missing))
