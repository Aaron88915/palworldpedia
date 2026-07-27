#!/usr/bin/env python3
"""
Process beckerfelipee AllCombos.csv into our breeding edges format.

Source: https://github.com/beckerfelipee/PalworldBreedingCalculator
- Data/AllCombos.csv  (semicolon-separated matrix, no header, UTF-8-BOM)
- Data/Pals.csv       (one pal name per line, roster = column/row order)
- Game version: 1.0.0

Output: {p1_slug, p2_slug, child_slug}[] sorted by p1,p2 alphabetically
"""
import csv
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
RAW_DIR = ROOT / 'scripts'
OUT = ROOT / 'public' / 'breeding-data.json'
PALS_JSON = ROOT / 'src' / 'data' / 'pals.json'

# Load our existing pals.json to map English name → our slug/ID
with open(PALS_JSON, 'r', encoding='utf-8') as f:
    pals_data = json.load(f)

# Build name → slug lookup. Match by English name (case-insensitive).
name_to_slug = {}
slug_to_pal = {}
for p in pals_data:
    en = p['name']['en'].lower().strip()
    name_to_slug[en] = p['id']
    slug_to_pal[p['id']] = p
    # Also try slug directly
    if p.get('id'):
        name_to_slug[p['id'].lower()] = p['id']

print(f'Loaded {len(pals_data)} pals from our pals.json')
print(f'Name→slug lookup size: {len(name_to_slug)}')

# Load beckerfelipee roster (Pals.csv)
roster_path = RAW_DIR / 'raw-beckerfelipee-Pals.csv'
with open(roster_path, 'r', encoding='utf-8-sig') as f:
    roster = [line.strip() for line in f if line.strip()]
print(f'Beckerfelipee roster size: {len(roster)}')

# Show new pals not in our DB
missing_in_ours = []
for pal in roster:
    if pal.lower() not in name_to_slug:
        missing_in_ours.append(pal)
if missing_in_ours:
    print(f'\n⚠ Pals in Beckerfelipee but NOT in our DB ({len(missing_in_ours)}):')
    for p in missing_in_ours[:20]:
        print(f'  - {p}')
    if len(missing_in_ours) > 20:
        print(f'  ... and {len(missing_in_ours) - 20} more')

# Show our pals not in Beckerfelipee (might be 1.0 added later)
in_becker = {p.lower() for p in roster}
ours_not_in_becker = []
for p in pals_data:
    en = p['name']['en'].lower().strip()
    if en not in in_becker:
        ours_not_in_becker.append((p['id'], p['name']['en']))
if ours_not_in_becker:
    print(f'\nPals in our DB but NOT in Beckerfelipee ({len(ours_not_in_becker)}):')
    for s, n in ours_not_in_becker[:30]:
        print(f'  - {s} ({n})')
    if len(ours_not_in_becker) > 30:
        print(f'  ... and {len(ours_not_in_becker) - 30} more')

# Load AllCombos matrix
matrix_path = RAW_DIR / 'raw-beckerfelipee-AllCombos.csv'
with open(matrix_path, 'r', encoding='utf-8-sig') as f:
    reader = csv.reader(f, delimiter=';')
    matrix = [row for row in reader]

print(f'\nMatrix shape: {len(matrix)} rows × {len(matrix[0]) if matrix else 0} cols')
assert len(matrix) == len(roster), f'Matrix rows ({len(matrix)}) != roster size ({len(roster)})'

# Convert to edges (upper triangle only, since matrix is symmetric)
edges = []
unmapped_parents = set()
unmapped_children = set()
for row in range(len(roster)):
    if len(matrix[row]) != len(roster):
        print(f'⚠ Row {row} has {len(matrix[row])} cols (expected {len(roster)})')
        continue
    for col in range(row, len(roster)):  # upper triangle
        parent1_en = roster[row]
        parent2_en = roster[col]
        child_en = matrix[row][col]

        p1_slug = name_to_slug.get(parent1_en.lower())
        p2_slug = name_to_slug.get(parent2_en.lower())
        c_slug = name_to_slug.get(child_en.lower())

        if not p1_slug:
            unmapped_parents.add(parent1_en)
        if not p2_slug:
            unmapped_parents.add(parent2_en)
        if not c_slug:
            unmapped_children.add(child_en)

        if p1_slug and p2_slug and c_slug:
            # Always store alphabetically to dedupe
            a, b = sorted([p1_slug, p2_slug])
            edges.append({'p1': a, 'p2': b, 'c': c_slug})

if unmapped_parents:
    print(f'\n⚠ Unmapped parents ({len(unmapped_parents)}): {sorted(unmapped_parents)[:10]}')
if unmapped_children:
    print(f'⚠ Unmapped children ({len(unmapped_children)}): {sorted(unmapped_children)[:10]}')

# Dedupe
unique_edges = {(e['p1'], e['p2']): e for e in edges}
edges_deduped = sorted(unique_edges.values(), key=lambda e: (e['p1'], e['p2']))
print(f'\nTotal edges (raw): {len(edges)}, deduped: {len(edges_deduped)}')

# Override: use 'c' as the child key (compact)
edges_deduped = [{'p1': e['p1'], 'p2': e['p2'], 'c': e['c']} for e in edges_deduped]

# Save compact format
with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(edges_deduped, f, ensure_ascii=False, separators=(',', ':'))

print(f'Wrote {OUT} ({os.path.getsize(OUT) / 1024:.1f} KB)')

# Compare with our existing breeding.json
our_breeding_path = ROOT / 'src' / 'data' / 'breeding.json'
if our_breeding_path.exists():
    with open(our_breeding_path, 'r', encoding='utf-8') as f:
        our_breeding = json.load(f)
    # Our existing format might be different - check
    print(f'\nOur existing format: {type(our_breeding)}')
    if isinstance(our_breeding, list) and our_breeding:
        print(f'Sample edge: {our_breeding[0]}')
        our_set = set()
        for e in our_breeding:
            if 'p1' in e and 'p2' in e:
                a, b = sorted([e['p1'], e['p2']])
                our_set.add((a, b))
        new_set = {(e['p1'], e['p2']) for e in edges_deduped}
        print(f'Our existing edges: {len(our_breeding)} (unique pairs: {len(our_set)})')
        print(f'Beckerfelipee edges: {len(edges_deduped)}')
        print(f'In both: {len(our_set & new_set)}')
        print(f'Only in ours: {len(our_set - new_set)}')
        print(f'Only in becker: {len(new_set - our_set)}')

# Quick test: Celaray + Lifmunk
print('\n--- Test: Celaray + Lifmunk = ? ---')
matches = [e for e in edges_deduped if {e['p1'], e['p2']} == {'celaray', 'lifmunk'}]
print(f'Matches: {matches}')

# Quick test: same parent combos
print('\n--- Test: Lamball + Lamball = ? ---')
matches = [e for e in edges_deduped if {e['p1'], e['p2']} == {'lamball', 'lamball'}]
print(f'Matches: {matches}')

# Quick test: Katress + Wixen (gender-dependent, should be one of them)
print('\n--- Test: Katress + Wixen = ? ---')
matches = [e for e in edges_deduped if {e['p1'], e['p2']} == {'katress', 'wixen'}]
print(f'Matches: {matches}')
