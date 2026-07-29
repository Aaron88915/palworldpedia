# -*- coding: utf-8 -*-
"""Extract work data from palworld.gg JSON - v2 with better parsing."""
import json, re

with open('scripts/palworldgg-bundles/CK2A4_hG.js', encoding='utf-8') as f:
    d = f.read()

# Split by pal object boundary
# Each pal starts with {id:"...",key:"...",
# Use a simple state machine
import re

# Find all name + work pairs
# Each pal object has: {id:"...",key:"...",slug:"...",name:"...",...,work:{...},...}
pal_pattern = re.compile(r'name:"([^"]+)",[^}]+?work:\{([^}]+)\}', re.DOTALL)
matches = pal_pattern.findall(d)
print(f'Total pal matches: {len(matches)}')

electricity = []
medicine = []
for name, work_str in matches:
    # Look for GenerateElectricity: N
    m = re.search(r'GenerateElectricity:(\d+)', work_str)
    if m and int(m.group(1)) > 0:
        electricity.append((name, int(m.group(1))))
    m = re.search(r'MedicineProduction:(\d+)', work_str)
    if m and int(m.group(1)) > 0:
        medicine.append((name, int(m.group(1))))

print(f'\nElectricity: {len(electricity)}')
for n, lvl in sorted(electricity):
    print(f'  {n:30s} Lv {lvl}')
print(f'\nMedicine: {len(medicine)}')
for n, lvl in sorted(medicine):
    print(f'  {n:30s} Lv {lvl}')
