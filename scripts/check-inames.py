# -*- coding: utf-8 -*-
import json
db = json.load(open('scripts/raw-palcalc-db.json', encoding='utf-8'))
for p in db['Pals']:
    if p['Name'] in ['Lamball', 'Green slime', 'Cattiva', 'Lifmunk']:
        n = p['Name']
        i = p['InternalName']
        bp = p.get('BreedingPower')
        print(f'  Name={n:20s} | InternalName={i:30s} | BP={bp}')
print('---')
for p in db['Pals'][:15]:
    n = p['Name']
    i = p['InternalName']
    bp = p.get('BreedingPower')
    print(f'  {i:30s} | Name={n:20s} | BP={bp}')
