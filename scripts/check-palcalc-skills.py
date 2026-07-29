import json
db = json.load(open('scripts/raw-palcalc-db.json', 'r', encoding='utf-8'))
print(f'Version: {db.get("Version")}')
print(f'Top-level keys: {list(db.keys())}')

# Find PlantSlime entries
print('\n=== PlantSlime entries ===')
for p in db['Pals']:
    if 'PlantSlime' in p.get('InternalName', ''):
        print(f'  {p["Name"]:30s} int={p["InternalName"]}  zh={p["LocalizedNames"].get("zh-Hans")}  HP={p.get("Hp")}')

# Check sample pal keys
print(f'\nSample pal all keys: {list(db["Pals"][0].keys())}')

# Check if there are skills in any pal (try with int_name)
for p in db['Pals'][:5]:
    sample_dict = p
    skill_keys = [k for k in sample_dict.keys() if 'kill' in k.lower() or 'active' in k.lower() or 'passive' in k.lower()]
    if skill_keys:
        print(f'  {p["Name"]}: skill keys = {skill_keys}')

# Check breeding.json for skill data
import os
if os.path.exists('scripts/raw-palcalc-breeding.json'):
    print('\n=== breeding.json structure ===')
    b = json.load(open('scripts/raw-palcalc-breeding.json', 'r', encoding='utf-8'))
    print(f'Keys: {list(b.keys())}')
    if b.get('Breeding'):
        # Find a sample with Parent2Gender != WILDCARD (specific gender)
        for entry in b['Breeding'][:20]:
            if entry.get('Parent1Gender') != 'WILDCARD' or entry.get('Parent2Gender') != 'WILDCARD':
                print(f'  Sample gender-specific: {entry}')
                break
        # Check structure
        print(f'\nBreeding entry keys: {list(b["Breeding"][0].keys())}')

    # Look for skills
    if b.get('ActiveSkills'):
        print(f'\nActiveSkills: {len(b["ActiveSkills"])} entries')
        print(f'Sample: {b["ActiveSkills"][0] if b["ActiveSkills"] else "none"}')
    if b.get('PassiveSkills'):
        print(f'PassiveSkills: {len(b["PassiveSkills"])} entries')
