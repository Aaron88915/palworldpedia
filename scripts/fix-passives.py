#!/usr/bin/env python3
"""
Re-enrich: palcalc only has GuaranteedPassives, not PartnerSkill.
Clear the partner-skill placeholder; properly populate passives from GuaranteedPassivesInternalIds.
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
PALS_JSON = ROOT / 'src' / 'data' / 'pals.json'
PALS_DATA = ROOT / 'public' / 'pals-data.json'
RAW_DIR = ROOT / 'scripts'

db = json.load(open(RAW_DIR / 'raw-palcalc-db.json', 'r', encoding='utf-8'))

def safe(s, kind='passive'):
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
        'description': {
            'zh': desc_loc.get('zh-Hans', ''),
            'en': s.get('Description', '') or '',
        }
    }

passive_catalog = {p['InternalName']: safe(p, 'passive') for p in db.get('PassiveSkills', [])}

palcalc_by_name = {p['Name']: p for p in db['Pals']}
palcalc_by_internal = {p['InternalName']: p for p in db['Pals']}

pals = json.load(open(PALS_JSON, 'r', encoding='utf-8'))

enriched = 0
unmatched = []
partner_count = 0
passive_count = 0

for p in pals:
    our_id = p['id']
    our_en = p['name']['en'].lower()

    pc = None
    # Match by English name
    for name, entry in palcalc_by_name.items():
        if name.lower() == our_en:
            pc = entry
            break
    # Fuzzy: name with spaces = our id with dashes
    if not pc:
        for name, entry in palcalc_by_name.items():
            if name.lower().replace(' ', '') == our_id.replace('-', ''):
                pc = entry
                break
    if not pc and our_id == 'ribbuny':
        for variant in ('Ribbuny', 'Ribunny'):
            if variant in palcalc_by_name:
                pc = palcalc_by_name[variant]
                break
    # Special: gumoss-special -> PlantSlime_Flower
    if not pc and our_id == 'gumoss-special':
        pc = palcalc_by_internal.get('PlantSlime_Flower')

    if not pc:
        unmatched.append((our_id, our_en))
        # Clear fake data
        p['partnerSkill'] = None
        p['passives'] = []
        continue

    # Clear the old placeholder
    p['partnerSkill'] = None
    p['passives'] = []

    # Add guaranteed passives
    guaranteed_ints = pc.get('GuaranteedPassivesInternalIds', [])
    for pi in guaranteed_ints:
        if pi in passive_catalog:
            p['passives'].append(passive_catalog[pi])
            passive_count += 1

    enriched += 1

print(f'Enriched {enriched}/{len(pals)} pals')
print(f'Total passive skill entries: {passive_count}')
if unmatched:
    print(f'\nUnmatched ({len(unmatched)}):')
    for our_id, our_en in unmatched[:20]:
        print(f'  {our_id:25s} en={our_en}')

# Save
with open(PALS_JSON, 'w', encoding='utf-8') as f:
    json.dump(pals, f, ensure_ascii=False, indent=2)
print(f'\nSaved {PALS_JSON}')

# Verify Cryolinx Terra
cryo = next((p for p in pals if p['id'] == 'cryolinx-terra'), None)
if cryo:
    print(f'\nCryolinx Terra verification:')
    print(f'  HP/ATK/DEF: {cryo["stats"]["hp"]}/{cryo["stats"]["attack"]["melee"]}/{cryo["stats"]["defense"]}')
    print(f'  Passives: {len(cryo.get("passives", []))} entries')
    for ps in cryo.get('passives', []):
        print(f'    - {ps["name"]["zh"]} ({ps["id"]})')

gumoss = next((p for p in pals if p['id'] == 'gumoss-special'), None)
if gumoss:
    print(f'\nGumoss Special:')
    print(f'  HP/ATK/DEF: {gumoss["stats"]["hp"]}/{gumoss["stats"]["attack"]["melee"]}/{gumoss["stats"]["defense"]}')
    print(f'  Passives: {len(gumoss.get("passives", []))} entries')

# Compact pals-data.json
compact = []
for p in pals:
    item = {
        'id': p['id'],
        'zh': p['name']['zh'],
        'en': p['name']['en'],
        'types': p['types'],
        'img': p['image'],
        'partner': (p.get('partnerSkill') or {}).get('id', ''),
        'passives': [ps.get('id', '') for ps in p.get('passives', [])],
    }
    compact.append(item)
with open(PALS_DATA, 'w', encoding='utf-8') as f:
    json.dump(compact, f, ensure_ascii=False, separators=(',', ':'))
print(f'Saved {PALS_DATA}')
