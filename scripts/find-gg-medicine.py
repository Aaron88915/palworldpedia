# -*- coding: utf-8 -*-
"""Find all medicine production in palworld.gg data."""
import re

with open('scripts/palworldgg-bundles/CK2A4_hG.js', encoding='utf-8') as f:
    d = f.read()

# Find all MedicineProduction occurrences
for m in re.finditer(r'(name|slug):"([^"]+)"[^}]+?MedicineProduction:(\d+)', d):
    print(f'  {m.group(1)}: {m.group(2)}, Lv {m.group(3)}')

# More lenient: just look for the keyword and surrounding context
print('\n=== All MedicineProduction context ===')
for m in re.finditer(r'MedicineProduction:(\d+)', d):
    idx = m.start()
    ctx = d[max(0, idx-300):idx+50]
    # Find name
    name_m = re.search(r'name:"([^"]+)"', ctx)
    if name_m:
        print(f'  {name_m.group(1)}: Lv {m.group(1)}')

# Also check different forms
print('\n=== Other medicine-like terms ===')
for kw in ['Medicine', 'medicine', 'Drug', 'Heal']:
    cnt = d.count(kw)
    print(f'  {kw}: {cnt} occurrences')
