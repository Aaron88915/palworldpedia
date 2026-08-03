# -*- coding: utf-8 -*-
"""Classify the 113 pals-without-biomes into special / variant / base."""
import json, re

pals = json.load(open('src/data/pals.json', encoding='utf-8'))
need = [p for p in pals if not p.get('biomes')]
print('Total need biomes: %d' % len(need))

# Variant suffixes
VARIANT_SUFFIXES = [
    '_Dark', '_Ice', '_Fire', '_Electric', '_Grass', '_Ground', '_Dragon',
    '_Water', '_Blaze', '_Astral', '_Aqua', '_Special', '_Jelly',
    '_Stream', '_Alpine', '_Forest', '_Obsidian', '_Crystal', '_Fantasm',
    '_Storm', '_Shadow', '_Stone', '_King', '_Royal', '_Air', '_Emperor',
    '_Observer', '_Lovely', '_Crusher', '_Blockhead', '_Libero', '_Umbral',
    '_Master', '_Ryu', '_Primo',
    '_Terra', '_Cryst', '_Ignis', '_Lux', '_Noct', '_Botan', '_Gild', '_Hydro',
    '_1', '_2', '_3',
]

def is_variant(pid):
    for s in VARIANT_SUFFIXES:
        if pid.endswith(s):
            return True, pid[:-len(s)]
    return False, None

special = []   # paldeckNo 0 OR 201-203 OR explicitly special ids
variants = []  # suffix variant with paldeckNo 1-200
bases = []     # plain base pals with paldeckNo 1-200

for p in need:
    pid = p['id']
    pno = p.get('paldeckNo', 0)
    is_var, base_id = is_variant(pid)
    if pno == 0 or pno >= 201 or pid in ('green-slime', 'gumoss-special', 'neptilius', 'jetragon', 'panthalus'):
        special.append(p)
    elif is_var:
        variants.append((p, base_id))
    else:
        bases.append(p)

print('Special: %d' % len(special))
for p in special:
    print('  %s paldeckNo=%d types=%s' % (p['id'], p.get('paldeckNo', 0), p.get('types', [])))

print('Variants: %d' % len(variants))
for p, bid in variants:
    print('  %-30s -> base=%s' % (p['id'], bid))

print('Bases: %d' % len(bases))
for p in bases:
    print('  %-30s paldeckNo=%-3d types=%s' % (p['id'], p.get('paldeckNo', 0), p.get('types', [])))

# Check if variant's base exists in pals
print()
print('=== variant base availability ===')
for p, bid in variants:
    found = any(x['id'] == bid for x in pals)
    base_biomes = next((x.get('biomes', []) for x in pals if x['id'] == bid), None)
    print('  %-30s -> base=%s found=%s base_biomes=%s' % (p['id'], bid, found, base_biomes))
