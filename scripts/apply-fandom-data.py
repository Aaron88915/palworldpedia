# -*- coding: utf-8 -*-
"""Merge Fandom data (drops, partner, skills, biomes, food) into pals.json for the 16 missing pals."""
import json, re

# Load data
pals = json.load(open('src/data/pals.json', encoding='utf-8'))
fandom_data = json.load(open('scripts/fandom-missing-pals-v2.json', encoding='utf-8'))
db = json.load(open('scripts/raw-palcalc-db.json', encoding='utf-8'))

# Build skill catalog lookup
catalog_by_name = {}
for s in db['ActiveSkills']:
    catalog_by_name[s['Name']] = s
    zh = s.get('LocalizedNames', {}).get('zh-Hans', '')
    if zh:
        catalog_by_name[zh] = s

# Build element map (InternalName -> Chinese)
ELEMENT_MAP = {
    'Normal': 'neutral',
    'Fire': 'fire',
    'Water': 'water',
    'Grass': 'grass',
    'Electric': 'electric',
    'Ice': 'ice',
    'Ground': 'ground',
    'Dark': 'dark',
    'Dragon': 'dragon',
}

def slugify(s):
    s = re.sub(r'[^a-zA-Z0-9]+', '-', s.lower()).strip('-')
    return s

def build_skill(skill_entry):
    """Convert Fandom skill to full skill object."""
    name = skill_entry['name']
    level = skill_entry['level']
    cat = catalog_by_name.get(name, {})
    if not cat:
        # try without parenthetical like "Double Fang (Dark)"
        clean = re.sub(r'\s*\([^)]+\)$', '', name)
        cat = catalog_by_name.get(clean, {})
    if not cat:
        # Fallback
        return {
            'id': slugify(name),
            'name': {'zh': name, 'en': name},
            'level': level,
            'type': 'neutral',
            'power': 0,
            'cooldown': 0,
            'description': {'zh': '', 'en': ''},
        }
    element = ELEMENT_MAP.get(cat.get('ElementInternalName', 'Normal'), 'neutral')
    zh = cat.get('LocalizedNames', {}).get('zh-Hans', cat['Name'])
    return {
        'id': cat.get('InternalName', slugify(name)),
        'name': {'zh': zh, 'en': cat['Name']},
        'level': level,
        'type': element,
        'power': cat.get('Power', 0),
        'cooldown': int(cat.get('CooldownSeconds', 0)),
        'description': {'zh': '', 'en': ''},
    }

# Build partnerSkill object (just basic name; desc needs more work)
def build_partner(name, en_name):
    return {
        'id': slugify(name),
        'name': {'zh': name, 'en': en_name or name},
        'description': {'zh': '', 'en': ''},
    }

# Apply to pals.json
updated = 0
for slug, fd in fandom_data.items():
    pal = next((p for p in pals if p['id'] == slug), None)
    if not pal:
        print(f'WARN: {slug} not found in pals.json')
        continue

    # Update drops
    if fd.get('drops') and not pal.get('drops'):
        pal['drops'] = fd['drops']
    # Update food
    if fd.get('food') and (not pal.get('food') or pal['food'] == 0):
        pal['food'] = fd['food']
    # Update skills
    if fd.get('active_skills') and not pal.get('skills'):
        pal['skills'] = [build_skill(s) for s in fd['active_skills']]
    # Update biomes
    if fd.get('biomes') and not pal.get('biomes'):
        pal['biomes'] = fd['biomes']
    # Update partnerSkill
    if fd.get('partner_skill') and not pal.get('partnerSkill'):
        # Look up Chinese name from palcalc if possible
        ps_en = fd['partner_skill']
        # Check ActiveSkills catalog for "PartnerSkill" type? Actually partner skills are different
        # Use the English name as both for now
        pal['partnerSkill'] = build_partner(ps_en, ps_en)

    pal['updatedAt'] = '2026-07-28'
    updated += 1
    print(f"Updated {slug:25s}: drops={len(pal['drops'])} skills={len(pal['skills'])} biomes={len(pal['biomes'])}")

print(f'\nUpdated {updated} pals')

# Save
json.dump(pals, open('src/data/pals.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('Saved pals.json')

# Summary
print()
print('=== Remaining gaps ===')
still_missing = [p for p in pals
                 if not p.get('skills') or not p.get('drops') or not p.get('biomes')]
print(f'Pals with any empty field: {len(still_missing)}')
for p in still_missing:
    missing = []
    if not p.get('skills'): missing.append('skills')
    if not p.get('drops'): missing.append('drops')
    if not p.get('biomes'): missing.append('biomes')
    print(f"  {p['id']:30s} missing: {missing}")
