# -*- coding: utf-8 -*-
import json
pals = json.load(open('src/data/pals.json', encoding='utf-8'))
mining = [p for p in pals if p.get('workSuitability', {}).get('mining', 0) > 0]
print(f'Mining pals: {len(mining)}')
for p in mining[:10]:
    n = p['name']['zh']
    print(f'  {p["id"]:25s} 采矿 Lv{p["workSuitability"]["mining"]} - {n}')
print()
kindling = [p for p in pals if p.get('workSuitability', {}).get('kindling', 0) > 0]
print(f'Kindling pals: {len(kindling)}')
planting = [p for p in pals if p.get('workSuitability', {}).get('planting', 0) > 0]
print(f'Planting pals: {len(planting)}')
r5 = [p for p in pals if p.get('rarity') == 5]
print(f'\nRarity 5: {len(r5)}')
for p in r5:
    n = p['name']['zh']
    print(f'  {p["id"]:25s} - {n}')
