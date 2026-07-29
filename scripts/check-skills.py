import json, sys
sys.stdout.reconfigure(encoding='utf-8')
db = json.load(open('scripts/raw-palcalc-db.json', 'r', encoding='utf-8'))

print(f'ActiveSkills: {len(db.get("ActiveSkills", []))}')
print(f'PassiveSkills: {len(db.get("PassiveSkills", []))}')
print(f'Elements: {len(db.get("Elements", []))}')

print('\n=== Sample ActiveSkill ===')
print(json.dumps(db['ActiveSkills'][0], ensure_ascii=False, indent=2))

print('\n=== Sample PassiveSkill ===')
print(json.dumps(db['PassiveSkills'][0], ensure_ascii=False, indent=2))

print('\n=== All Elements ===')
for e in db['Elements']:
    print(f'  {e}')

# Check what fields a pal has - maybe it has internal name + a list of skills
# But we already saw: only GuaranteedPassivesInternalIds and PartnerSkill in pals
# So active skills are not linked per-pal in db.json. Hmm.

# Check breeding.json
import os
if os.path.exists('scripts/raw-palcalc-breeding.json'):
    b = json.load(open('scripts/raw-palcalc-breeding.json', 'r', encoding='utf-8'))
    print(f'\n=== breeding.json top keys: {list(b.keys())}')
    if b.get('Breeding'):
        print(f'Breeding entries: {len(b["Breeding"])}')
        print(f'Sample entry keys: {list(b["Breeding"][0].keys())}')

# Maybe MinBreedingSteps has skill info?
if b.get('MinBreedingSteps'):
    print(f'\nMinBreedingSteps sample: {b["MinBreedingSteps"][:2] if b["MinBreedingSteps"] else "none"}')
