#!/usr/bin/env python3
"""
Enrich pals.json with full data from palcalc db.json:
- HP, Defense, Attack, WalkSpeed, RunSpeed, RideSprintSpeed
- Price, Rarity, Size, Nocturnal
- MinWildLevel, MaxWildLevel
- WorkSuitability (dict)
- PartnerSkill, GuaranteedPassivesInternalIds
- LocalizedNames (zh-Hans) — already used for zh field
- PalDexNo (real numbers!)
- InternalName (cross-validation)
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
PALS_JSON = ROOT / 'src' / 'data' / 'pals.json'
PALCALC_DB = ROOT / 'scripts' / 'raw-palcalc-db.json'

# Map our ID -> palcalc Name (English display)
# These are the 17 newly added + 8 orphans that need enrichment
ID_TO_PALCALC_NAME = {
    # 17 new 1.0 pals (added in this session)
    'fuack':         'Fuack',
    'clovee':        'Clovee',
    'tanzee':        'Tanzee',
    'rooby':         'Rooby',
    'pupperai':      'Pupperai',
    'sparkit':       'Sparkit',
    'ribunny':       'Ribunny',  # was added as new (the typo was 'ribbuny')
    'foxparks-cryst':'Foxparks Cryst',
    'celaray-lux':   'Celaray Lux',
    'caprity-noct':  'Caprity Noct',
    'loupmoon-cryst':'Loupmoon Cryst',
    'fenglope-lux':  'Fenglope Lux',
    'dazzi-noct':    'Dazzi Noct',
    'dumud-gild':    'Dumud Gild',
    'kitsun-noct':   'Kitsun Noct',
    'cryolinx-terra':'Cryolinx Terra',
    'gumoss-special':'Gumoss (Special)',
    # 8 orphans (in our DB but missing data)
    'boltmane':      'Boltmane',
    'cyan-wolf-cub': 'Cyan Wolf Cub',
    'dark-mutant':   'Dark Mutant',
    'dragostrophe':  'Dragostrophe',
    'feathered-dragon':'Feathered Dragon',
    'green-slime':   'Green slime',
    'ribbuny':       'Ribbuny',  # the typo entry
    'astralym':      'Astralym',
}

# Element type mapping (from palcalc breeding.json ElementTypes to our lowercase)
# We'll figure out types from workSuitability patterns or just use the most reliable approach
# Since palcalc's db doesn't have explicit ElementTypes per pal, we use the InternalName suffix
# Variants end in: _Ice, _Dark, _Ground, _Fire, _Electric, _Water, _Dragon, _Leaf
TYPE_FROM_SUFFIX = {
    'Ice': 'ice', 'Cryst': 'ice',  # Cryst = ice variant
    'Dark': 'dark', 'Noct': 'dark',
    'Ground': 'ground', 'Terra': 'ground', 'Gild': 'dragon',  # Gild is special
    'Fire': 'fire', 'Ignis': 'fire',
    'Electric': 'electric', 'Lux': 'electric',
    'Water': 'water',
    'Dragon': 'dragon',
    'Leaf': 'grass',
    'Light': 'neutral',
}

# Variant suffix -> our naming convention
VARIANT_SUFFIX = {
    'Ignis': 'ignis',
    'Noct': 'noct',
    'Cryst': 'cryst',
    'Lux': 'lux',
    'Terra': 'terra',
    'Primo': 'primo',
    'Aqua': 'aqua',
    'Botan': 'botan',
    'Ryu': 'ryu',
    'Libero': 'libero',
}

# Load palcalc db
db = json.load(open(PALCALC_DB, 'r', encoding='utf-8'))
palcalc_by_name = {p['Name']: p for p in db['Pals']}

# Load our pals
pals = json.load(open(PALS_JSON, 'r', encoding='utf-8'))
our_by_id = {p['id']: p for p in pals}

print(f'Our pals: {len(pals)}')
print(f'Palcalc pals: {len(db["Pals"])}')

# Find element type from breeding.json (if available)
# Actually let's use workSuitability patterns + InternalName to guess
# But better: use the palcalc breeding.json which has ChildElement
BREEDING_JSON = ROOT / 'scripts' / 'raw-palcalc-breeding.json'
elem_by_internal = {}
if BREEDING_JSON.exists():
    print('Loading breeding.json for element types...')
    breeding = json.load(open(BREEDING_JSON, 'r', encoding='utf-8'))
    # Sample a few entries to see structure
    if breeding.get('Breeding'):
        first = breeding['Breeding'][0]
        print(f'  Sample breeding entry keys: {list(first.keys())[:10]}')
        for entry in breeding['Breeding']:
            child_int = entry.get('ChildInternalName', '').lower()
            elem = entry.get('ChildElement', '')
            if child_int and elem:
                elem_by_internal[child_int] = elem

print(f'  Element data: {len(elem_by_internal)} children')

def get_element(internal_name):
    """Get element from breeding data, or guess from internal name suffix."""
    il = internal_name.lower()
    if il in elem_by_internal:
        return elem_by_internal[il].lower()
    # Fallback: look at suffix
    parts = il.split('_')
    for p in parts[1:]:  # skip first (base name)
        if p.capitalize() in TYPE_FROM_SUFFIX:
            return TYPE_FROM_SUFFIX[p.capitalize()]
    return 'normal'

# WorkSuitability field normalization
WORK_FIELDS = [
    'Kindling', 'Watering', 'Planting', 'GenerateElectricity', 'Handiwork',
    'Gathering', 'Lumbering', 'Mining', 'MedicineProduction', 'Cooling',
    'Transporting', 'Farming',
]
def work_to_dict(ws):
    """Convert palcalc WorkSuitability dict to our format (lowercase keys, drop zeros)."""
    if not ws:
        return {}
    out = {}
    for k in WORK_FIELDS:
        v = ws.get(k, 0)
        if v and v > 0:
            # Map to our key naming (GenerateElectricity -> electricity)
            key_map = {'Kindling': 'kindling', 'Watering': 'watering',
                       'Planting': 'planting', 'GenerateElectricity': 'electricity',
                       'Handiwork': 'handiwork', 'Gathering': 'gathering',
                       'Lumbering': 'lumbering', 'Mining': 'mining',
                       'MedicineProduction': 'medicine', 'Cooling': 'cooling',
                       'Transporting': 'transporting', 'Farming': 'farming'}
            out[key_map.get(k, k.lower())] = v
    return out

def skill_to_our(pal, palcalc_entry):
    """Build a skill list. We don't have skill translations yet, so use en names.
    We use the ActiveSkills from db if available, or just placeholder."""
    # Palcalc's db has 'ActiveSkills' embedded? Let me check
    skills = palcalc_entry.get('ActiveSkills', [])
    if not skills:
        # Try to get skills from another field
        return []
    out = []
    for s in skills:
        out.append({
            'id': s.get('InternalName', '').lower(),
            'name': {'zh': s.get('Name', ''), 'en': s.get('Name', '')},
            'level': 1,
            'type': s.get('ElementInternalName', '').lower(),
            'power': s.get('Power', 0),
        })
    return out

# Try to load active skills from palcalc's actual full data
# (db.json doesn't have skills; need breeding.json or another source)

# Enrich each of our 25 target pals
enriched = []
unmatched = []
for our_id, palcalc_name in ID_TO_PALCALC_NAME.items():
    if our_id not in our_by_id:
        print(f'  ! Our pal "{our_id}" not in DB, skipping')
        continue
    p = our_by_id[our_id]
    pc = palcalc_by_name.get(palcalc_name)
    if not pc:
        print(f'  ! Palcalc name "{palcalc_name}" not found, skipping')
        unmatched.append((our_id, palcalc_name))
        continue

    old = {
        'paldeckNo': p['paldeckNo'],
        'types': p['types'],
        'hp': p['stats'].get('hp', 0),
        'attack': p['stats'].get('attack', {}).get('melee', 0) if isinstance(p['stats'].get('attack'), dict) else 0,
        'defense': p['stats'].get('defense', 0),
        'walkSpeed': p['stats'].get('speed', 0),
        'rarity': p['rarity'],
        'workSuitability': p['workSuitability'],
    }

    # Update fields
    p['paldeckNo'] = pc['Id']['PalDexNo']
    # Element type
    elem = get_element(pc['InternalName'])
    # Use element from palcalc data
    if pc['InternalName'].lower() in elem_by_internal:
        elem = elem_by_internal[pc['InternalName'].lower()].lower()
    p['types'] = [elem]
    p['stats'] = {
        'hp': pc.get('Hp', 0),
        'attack': {
            'melee': pc.get('Attack', 0),
            'ranged': 0,  # palcalc doesn't have ranged separately
        },
        'defense': pc.get('Defense', 0),
        'speed': pc.get('RunSpeed', 0) or pc.get('WalkSpeed', 0),
    }
    p['rarity'] = pc.get('Rarity', 1)
    p['workSuitability'] = work_to_dict(pc.get('WorkSuitability', {}))
    p['price'] = pc.get('Price', 0)
    p['food'] = pc.get('FoodAmount', 0)

    # Size: XS/S/M/L -> chinese
    size_map = {'XS': 'XS', 'S': 'S', 'M': 'M', 'L': 'L'}
    p['size'] = size_map.get(pc.get('Size', 'M'), 'M')

    # nightOnly
    p['nightOnly'] = pc.get('Nocturnal', False)

    # Description (placeholder since palcalc doesn't have full desc)
    if not p.get('description', {}).get('zh'):
        p['description'] = p.get('description', {'zh': '', 'en': ''})

    # Note: We have empty passives/skills/drops/biomes - need another source for these
    # Mark as "needs-fandom-wiki" for now
    p['updatedAt'] = '2026-07-28'

    enriched.append((our_id, palcalc_name, old, {
        'paldeckNo': p['paldeckNo'],
        'types': p['types'],
        'hp': p['stats']['hp'],
        'attack': p['stats']['attack']['melee'],
        'defense': p['stats']['defense'],
        'rarity': p['rarity'],
    }))

# Save
with open(PALS_JSON, 'w', encoding='utf-8') as f:
    json.dump(pals, f, ensure_ascii=False, indent=2)

print(f'\nEnriched {len(enriched)} pals:')
for our_id, palcalc_name, old, new in enriched:
    print(f'  {our_id:20s} | deck {old["paldeckNo"]:>3} -> {new["paldeckNo"]:<3} | '
          f'types {old["types"]} -> {new["types"]} | '
          f'HP {old["hp"]:>4} -> {new["hp"]:<4} | '
          f'ATK {old["attack"]:>3} -> {new["attack"]:<3} | '
          f'DEF {old["defense"]:>3} -> {new["defense"]:<3}')

if unmatched:
    print(f'\nUnmatched ({len(unmatched)}):')
    for our_id, pn in unmatched:
        print(f'  {our_id} -> {pn}')
