# -*- coding: utf-8 -*-
import json
pals = json.load(open('src/data/pals.json', encoding='utf-8'))
print('Pals with rarity >= 5:')
for p in pals:
    if p.get('rarity', 0) >= 5:
        en = p.get('name', {}).get('en', '?')
        print(f'  {p["id"]:30s} | {en:30s} | rarity={p["rarity"]} | paldeckNo={p.get("paldeckNo")}')

print()
db = json.load(open('scripts/raw-palcalc-db.json', encoding='utf-8'))
print('palcalc Rarity field for the 5+ pals:')
for p in db['Pals']:
    if p.get('Rarity', 0) >= 5:
        print(f'  {p.get("InternalName"):30s} | {p.get("Name"):30s} | Rarity={p.get("Rarity")} | ID={p.get("Id")}')
