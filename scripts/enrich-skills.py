#!/usr/bin/env python3
"""
Enrich pals.json with:
1. PartnerSkill (per-pal) - linked to PassiveSkills catalog
2. GuaranteedPassives (per-pal) - linked to PassiveSkills catalog
3. Fix Gumoss Special (find in palcalc by InternalName)
4. Save skills/passives catalogs to /public for frontend use
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
PALS_JSON = ROOT / 'src' / 'data' / 'pals.json'
PALS_DATA = ROOT / 'public' / 'pals-data.json'
SKILLS_DATA = ROOT / 'public' / 'skills-data.json'
RAW_DIR = ROOT / 'scripts'

db = json.load(open(RAW_DIR / 'raw-palcalc-db.json', 'r', encoding='utf-8'))

# Build catalogs
passives = {p['InternalName']: p for p in db.get('PassiveSkills', [])}
actives = {a['InternalName']: a for a in db.get('ActiveSkills', [])}

# Build compact skills catalog for frontend
def to_skill(s, kind):
    if not s:
        return None
    loc = s.get('LocalizedNames') or {}
    desc_loc = s.get('LocalizedDescriptions') or {}
    return {
        'id': (s.get('InternalName') or '').lower(),
        'name': {
            'zh': loc.get('zh-Hans') or s.get('Name', ''),
            'en': s.get('Name', ''),
        },
        'desc': desc_loc.get('zh-Hans', '') if kind == 'passive' else '',
    }

passive_catalog = {k: to_skill(v, 'passive') for k, v in passives.items()}
active_catalog = {k: to_skill(v, 'active') for k, v in actives.items()}

print(f'Passives: {len(passive_catalog)}, Actives: {len(active_catalog)}')

# Save skills catalog
skills_export = {
    'passives': passive_catalog,
    'actives': active_catalog,
}
with open(SKILLS_DATA, 'w', encoding='utf-8') as f:
    json.dump(skills_export, f, ensure_ascii=False, separators=(',', ':'))
print(f'Wrote {SKILLS_DATA} ({len(json.dumps(skills_export)) / 1024:.1f} KB)')

# Load pals
pals = json.load(open(PALS_JSON, 'r', encoding='utf-8'))

# Build palcalc name -> entry map (and internal -> name map)
palcalc_by_name = {p['Name']: p for p in db['Pals']}
palcalc_by_internal = {p['InternalName']: p for p in db['Pals']}

# Map our ID -> palcalc name (and internal)
ID_TO_PALCALC = {
    # 17 new 1.0 pals
    'fuack':         ('Fuack', 'BluePlatypus'),
    'clovee':        ('Clovee', 'CloverFairy'),
    'tanzee':        ('Tanzee', 'Monkey'),
    'rooby':         ('Rooby', 'FlameBambi'),
    'pupperai':      ('Pupperai', 'SamuraiDog'),
    'sparkit':       ('Sparkit', 'ElecCat'),
    'foxparks-cryst':('Foxparks Cryst', 'Kitsunebi_Ice'),
    'celaray-lux':   ('Celaray Lux', 'FlyingManta_Thunder'),
    'caprity-noct':  ('Caprity Noct', 'BerryGoat_Dark'),
    'loupmoon-cryst':('Loupmoon Cryst', 'Werewolf_Ice'),
    'fenglope-lux':  ('Fenglope Lux', 'FengyunDeeper_Electric'),
    'dazzi-noct':    ('Dazzi Noct', 'RaijinDaughter_Water'),
    'dumud-gild':    ('Dumud Gild', 'LazyCatfish_Gold'),
    'kitsun-noct':   ('Kitsun Noct', 'AmaterasuWolf_Dark'),
    'cryolinx-terra':('Cryolinx Terra', 'WhiteTiger_Ground'),
    'gumoss-special':(None, 'PlantSlime_Flower'),  # special - find by internal
    'ribbuny':       ('Ribbuny', None),  # already enriched
    # Also enrich all 288 with partner skill
}

def get_palcalc(our_id):
    if our_id not in ID_TO_PALCALC:
        return None
    pc_name, int_name = ID_TO_PALCALC[our_id]
    if pc_name and pc_name in palcalc_by_name:
        return palcalc_by_name[pc_name]
    if int_name and int_name in palcalc_by_internal:
        return palcalc_by_internal[int_name]
    return None

# Enrich 17 new + Gumoss Special
enriched_count = 0
for p in pals:
    pc = get_palcalc(p['id'])
    if not pc:
        continue

    old_hp = p['stats'].get('hp', 0)
    p['stats'] = {
        'hp': pc.get('Hp', 0),
        'attack': {
            'melee': pc.get('Attack', 0),
            'ranged': 0,
        },
        'defense': pc.get('Defense', 0),
        'speed': pc.get('RunSpeed', 0) or pc.get('WalkSpeed', 0),
    }
    p['rarity'] = pc.get('Rarity', 1)
    p['price'] = pc.get('Price', 0)
    p['food'] = pc.get('FoodAmount', 0)

    # Partner skill (passive skill that's unique to this pal)
    partner_int = pc.get('PartnerSkill')
    if partner_int and partner_int in passive_catalog:
        p['partnerSkill'] = passive_catalog[partner_int]

    # Guaranteed passives
    guaranteed_ints = pc.get('GuaranteedPassivesInternalIds', [])
    guaranteed = []
    for pi in guaranteed_ints:
        if pi in passive_catalog:
            guaranteed.append(passive_catalog[pi])
    if guaranteed:
        p['passives'] = guaranteed

    enriched_count += 1

print(f'\nEnriched {enriched_count} pals (partner skill + guaranteed passives)')

# Save
with open(PALS_JSON, 'w', encoding='utf-8') as f:
    json.dump(pals, f, ensure_ascii=False, indent=2)
print(f'Saved {PALS_JSON}')

# Also save compact pals-data.json with partner/passive IDs
# (frontend can fetch skills catalog separately and look up)
compact = []
for p in pals:
    item = {
        'id': p['id'],
        'zh': p['name']['zh'],
        'en': p['name']['en'],
        'types': p['types'],
        'img': p['image'],
        'partner': p.get('partnerSkill', {}).get('id', '') if p.get('partnerSkill') else '',
        'passives': [ps.get('id', '') for ps in p.get('passives', [])],
    }
    compact.append(item)
with open(PALS_DATA, 'w', encoding='utf-8') as f:
    json.dump(compact, f, ensure_ascii=False, separators=(',', ':'))
print(f'Saved {PALS_DATA}')

# Verify Gumoss Special specifically
gumoss = next((p for p in pals if p['id'] == 'gumoss-special'), None)
if gumoss:
    print(f'\nGumoss Special HP/ATK/DEF: {gumoss["stats"]["hp"]}/{gumoss["stats"]["attack"]["melee"]}/{gumoss["stats"]["defense"]}')

# Verify Cryolinx Terra
cryolinx = next((p for p in pals if p['id'] == 'cryolinx-terra'), None)
if cryolinx:
    print(f'Cryolinx Terra HP/ATK/DEF: {cryolinx["stats"]["hp"]}/{cryolinx["stats"]["attack"]["melee"]}/{cryolinx["stats"]["defense"]}')
    print(f'  Partner: {cryolinx.get("partnerSkill", {}).get("name", {}).get("zh", "")}')
    print(f'  Passives: {[p["name"]["zh"] for p in cryolinx.get("passives", [])]}')
