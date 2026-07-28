#!/usr/bin/env python3
"""Find palcalc's actual name for unmatched pals + check element types."""
import json
db = json.load(open('scripts/raw-palcalc-db.json', 'r', encoding='utf-8'))
m = {p['Name']: p for p in db['Pals']}

# Print all palcalc pals to find matches
candidates = ['Boltmane', 'Cyan Wolf Cub', 'Dark Mutant', 'Dragostrophe',
              'Feathered Dragon', 'Green slime', 'Astralym', 'Ribunny', 'Gumoss (Special)']
for c in candidates:
    # Try exact
    e = m.get(c)
    if e:
        print(f'  EXACT: {c} -> int={e["InternalName"]}, deck={e["Id"]["PalDexNo"]}, isVariant={e["Id"]["IsVariant"]}, BP={e["BreedingPower"]}')
    else:
        # Try case-insensitive partial
        for n, p in m.items():
            if c.lower() in n.lower():
                print(f'  PARTIAL: {c} -> {n} (int={p["InternalName"]}, deck={p["Id"]["PalDexNo"]}, variant={p["Id"]["IsVariant"]}, BP={p["BreedingPower"]})')
                break
        else:
            print(f'  NOT FOUND: {c}')

# Also: list all pals to look for element type field
print('\n=== Looking for element info in palcalc ===')
sample = list(m.values())[0]
print(f'Sample pal keys: {list(sample.keys())}')
print()

# Check if BreedingPower is related to type (high = common)
# Actually look for ElementTypes in any pal
for p in m.values():
    if 'ElementTypes' in p and p['ElementTypes']:
        print(f'Found ElementTypes in {p["Name"]}: {p["ElementTypes"]}')
        break
print()

# Look for Type1/Type2 in any pal
for p in m.values():
    for k in ('Type1', 'Type2', 'Element1', 'Element2'):
        if k in p and p[k]:
            print(f'Found {k} in {p["Name"]}: {p[k]}')
            break

# Actually let me check the breeding.json (not yet downloaded)
print('\n=== Palcalc InternalName samples (look for type suffix) ===')
for p in db['Pals'][:15]:
    print(f'  {p["Name"]:30s} -> int={p["InternalName"]}')
