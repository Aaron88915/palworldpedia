import json
db = json.load(open('scripts/raw-palcalc-db.json', 'r', encoding='utf-8'))

# Check a few pals
for pname in ['Lamball', 'Nyafia', 'Cattiva', 'Foxparks Cryst', 'Anubis']:
    p = next((x for x in db['Pals'] if x['Name'] == pname), None)
    if p:
        partner = p.get('PartnerSkill')
        guaranteed = p.get('GuaranteedPassivesInternalIds', [])
        print(f'{pname:20s}: Partner={partner}, Guaranteed={guaranteed[:2]}')

# Check if PartnerSkill names match PassiveSkills
ps_names = {ps['InternalName'] for ps in db['PassiveSkills']}
print(f'\nPassiveSkill names sample: {list(ps_names)[:5]}')

# Check what types of PartnerSkill values exist
partner_values = set()
for p in db['Pals']:
    if p.get('PartnerSkill'):
        partner_values.add(p['PartnerSkill'])
print(f'\nUnique PartnerSkill values: {len(partner_values)}')
for v in list(partner_values)[:10]:
    print(f'  {v!r}')
