#!/usr/bin/env python3
"""
Comprehensive enrichment: link all 288 pals to palcalc PartnerSkill + GuaranteedPassives.
For active skills / drops / biomes — data not in palcalc, will need other source later.
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
        'desc': desc_loc.get('zh-Hans', '') if kind == 'passive' else '',
    }

passive_catalog = {p['InternalName']: safe(p, 'passive') for p in db.get('PassiveSkills', [])}

# Build name and internal lookup from palcalc
palcalc_by_name = {p['Name']: p for p in db['Pals']}
palcalc_by_internal = {p['InternalName']: p for p in db['Pals']}

# Build our ID -> palcalc entry map
pals = json.load(open(PALS_JSON, 'r', encoding='utf-8'))

# Strategy: try to match by our ID (lowercase) against palcalc name (lowercase with space)
# And also by our existing internal name
enriched = 0
unmatched = []
for p in pals:
    our_id = p['id']
    our_en = p['name']['en'].lower()
    our_int = our_id.replace('-', '_')  # celaray-lux -> celaray_lux (but palcalc uses CamelCase)

    # Try to find in palcalc
    pc = None
    # 1. Try by English name (exact, case-insensitive)
    for name, entry in palcalc_by_name.items():
        if name.lower() == our_en:
            pc = entry
            break
    # 2. Try by internal name (we have it in our data via... hmm we don't store internalName)
    # 3. Try by fuzzy match
    if not pc:
        # Map common: our_id = "ribbuny" -> palcalc might have "Ribbuny" or "Ribunny"
        for name, entry in palcalc_by_name.items():
            if name.lower().replace(' ', '') == our_id.replace('-', ''):
                pc = entry
                break
    # 4. Map our "ribbuny" typo to "Ribunny" in palcalc (or "Ribbuny")
    if not pc and our_id == 'ribbuny':
        for variant in ('Ribbuny', 'Ribunny'):
            if variant in palcalc_by_name:
                pc = palcalc_by_name[variant]
                break

    if not pc:
        unmatched.append((our_id, our_en))
        continue

    # Update partner skill and passives
    partner_int = pc.get('PartnerSkill')
    if partner_int and partner_int in passive_catalog:
        p['partnerSkill'] = passive_catalog[partner_int]
    else:
        # No partner skill (clear any old data)
        p['partnerSkill'] = None

    guaranteed_ints = pc.get('GuaranteedPassivesInternalIds', [])
    guaranteed = []
    for pi in guaranteed_ints:
        if pi in passive_catalog:
            guaranteed.append(passive_catalog[pi])
    p['passives'] = guaranteed

    enriched += 1

print(f'Enriched {enriched}/{len(pals)} pals')
if unmatched:
    print(f'\nUnmatched ({len(unmatched)}):')
    for our_id, our_en in unmatched[:30]:
        print(f'  {our_id:25s} en={our_en}')

# Save
with open(PALS_JSON, 'w', encoding='utf-8') as f:
    json.dump(pals, f, ensure_ascii=False, indent=2)
print(f'\nSaved {PALS_JSON}')

# Save compact pals-data.json
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

# Quick stats
total_partner = sum(1 for p in pals if p.get('partnerSkill'))
total_passives = sum(len(p.get('passives', [])) for p in pals)
print(f'\nTotal pals with partner skill: {total_partner}/{len(pals)}')
print(f'Total passive skill entries: {total_passives}')
