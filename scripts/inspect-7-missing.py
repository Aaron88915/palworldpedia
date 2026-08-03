#!/usr/bin/env python3
import json
pals = json.load(open('src/data/pals.json', encoding='utf-8'))
targets = ['Pengullet Lux', 'Xenovader', 'Xenogard', 'Bellanoir', 'Bellanoir Libero', 'Xenolord', 'Hartalis']
print('=== 7 missing pals ===')
for p in pals:
    if p['name']['en'] in targets:
        print(f'# {p["paldeckNo"]} zh={p["name"]["zh"]} en={p["name"]["en"]} types={p.get("types",[])} rarity={p.get("rarity")} biomes={p.get("biomes")}')

print()
print('=== base Pengullet (for variant copy) ===')
for p in pals:
    if p['name']['en'] == 'Pengullet':
        print(f'# {p["paldeckNo"]} biomes={p.get("biomes")}')

print()
print('=== Boss / Tower pals in data ===')
for p in pals:
    if any(k in p['name']['en'] for k in ['Xeno','Bellanoir','Hartalis','Paladius','Necromus','Faleris','Silveon']):
        print(f'# {p["paldeckNo"]} {p["name"]["zh"]} ({p["name"]["en"]}) biomes={p.get("biomes")}')

print()
print('=== Unique biome names in data ===')
uniq = set()
for p in pals:
    for b in p.get('biomes') or []:
        uniq.add(b)
for b in sorted(uniq):
    print(' -', b)
