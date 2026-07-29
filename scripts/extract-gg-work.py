# -*- coding: utf-8 -*-
"""Extract work data from palworld.gg JSON."""
import json, re

with open('scripts/palworldgg-bundles/CK2A4_hG.js', encoding='utf-8') as f:
    d = f.read()

# Each pal: work:{Watering: 1, ...}
# Find work blocks
electricity_pals = []
medicine_pals = []
all_works = set()
# Regex: find each pal's work block - look for "work:{...}"
pal_blocks = re.findall(r'(?:name|slug):"([^"]+)"[^}]*?work:\{([^}]+)\}', d)
for name, work_str in pal_blocks:
    work = {}
    for m in re.finditer(r'(\w+):(\d+)', work_str):
        work[m.group(1)] = int(m.group(2))
    if 'GenerateElectricity' in work and work['GenerateElectricity'] > 0:
        electricity_pals.append((name, work['GenerateElectricity']))
    if 'MedicineProduction' in work and work['MedicineProduction'] > 0:
        medicine_pals.append((name, work['MedicineProduction']))
    for w in work.keys():
        all_works.add(w)

print(f'All work keys in GG: {sorted(all_works)}')
print(f'\nElectricity pals ({len(electricity_pals)}):')
for n, lvl in sorted(electricity_pals):
    print(f'  {n:30s} Lv {lvl}')
print(f'\nMedicine pals ({len(medicine_pals)}):')
for n, lvl in sorted(medicine_pals):
    print(f'  {n:30s} Lv {lvl}')
