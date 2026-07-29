# -*- coding: utf-8 -*-
"""Extract ALL work data from palworld.gg bundle and merge into pals.json."""
import json, re

# Map palworld.gg work keys to our config keys
GG_TO_OURS = {
    'GenerateElectricity': 'generating_electricity',
    'ProductMedicine': 'medicine_production',
    'Handcraft': 'handiwork',
    'Transport': 'transporting',
    'Deforest': 'lumbering',
    'EmitFlame': 'kindling',
    'Watering': 'watering',
    'Seeding': 'planting',
    'Collection': 'gathering',
    'Mining': 'mining',
    'Cool': 'cooling',
    'MonsterFarm': 'farming',
}

with open('scripts/palworldgg-bundles/CK2A4_hG.js', encoding='utf-8') as f:
    d = f.read()

# Find all pal objects - match from slug to work block
# Pattern: slug:"NAME",...,work:{...}
# Use a more lenient approach - find work:{...} blocks associated with each pal

# First, find all work:{} blocks
work_blocks = re.findall(r'work:\{([^}]+)\}', d)
print(f'Total work blocks: {len(work_blocks)}')

# Parse each block
all_work = []
for wb in work_blocks:
    w = {}
    for m in re.finditer(r'(\w+):(\d+)', wb):
        key = m.group(1)
        if key in GG_TO_OURS:
            w[GG_TO_OURS[key]] = int(m.group(2))
    if w:
        all_work.append(w)

# Now find pal name and slug for each block
# Pattern: ...name:"X",...work:{...}
pal_data = []
# Better: find all slug/name pairs, then correlate
slug_to_idx = {}
for i, m in enumerate(re.finditer(r'slug:"([^"]+)"[^}]*?name:"([^"]+)"', d)):
    slug_to_idx[i] = (m.group(1), m.group(2))

# Different approach: split by pal boundary
# Each pal ends with },{ or end of array
# Find positions
pal_starts = [m.start() for m in re.finditer(r'id:"[a-z]+"', d)]
pal_starts.append(len(d))

print(f'Pal starts: {len(pal_starts)}')

# For each pal, extract name + work
results = []
for i in range(len(pal_starts) - 1):
    chunk = d[pal_starts[i]:pal_starts[i+1]]
    name_m = re.search(r'name:"([^"]+)"', chunk)
    work_m = re.search(r'work:\{([^}]+)\}', chunk)
    if name_m and work_m:
        name = name_m.group(1)
        work = {}
        for m in re.finditer(r'(\w+):(\d+)', work_m.group(1)):
            key = m.group(1)
            if key in GG_TO_OURS:
                work[GG_TO_OURS[key]] = int(m.group(2))
        if work:
            results.append((name, work))

print(f'Total pals with work: {len(results)}')

# Aggregate by name (sum levels - same pal might appear multiple times for variants)
name_to_work = {}
for name, work in results:
    if name not in name_to_work:
        name_to_work[name] = {}
    for k, v in work.items():
        name_to_work[name][k] = max(name_to_work[name].get(k, 0), v)

# Show electricity/medicine pals
print(f'\nGenerating electricity pals: {len([n for n, w in name_to_work.items() if w.get("generating_electricity", 0) > 0])}')
for n, w in sorted(name_to_work.items()):
    if w.get('generating_electricity', 0) > 0:
        print(f'  {n:30s} Lv {w["generating_electricity"]}')

print(f'\nMedicine pals: {len([n for n, w in name_to_work.items() if w.get("medicine_production", 0) > 0])}')
for n, w in sorted(name_to_work.items()):
    if w.get('medicine_production', 0) > 0:
        print(f'  {n:30s} Lv {w["medicine_production"]}')

# Save
with open('scripts/gg-work-by-name.json', 'w', encoding='utf-8') as f:
    json.dump(name_to_work, f, ensure_ascii=False, indent=2)
print(f'\nSaved scripts/gg-work-by-name.json ({len(name_to_work)} pals)')
