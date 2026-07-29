# -*- coding: utf-8 -*-
import json, os
new = json.load(open('src/data/pals.json', encoding='utf-8'))
print(f'New pals count: {len(new)}')
print(f'New file size: {os.path.getsize("src/data/pals.json")} bytes')
# Count fields with data
no_skills = sum(1 for p in new if not p.get('skills'))
no_drops = sum(1 for p in new if not p.get('drops'))
no_biomes = sum(1 for p in new if not p.get('biomes'))
no_partner = sum(1 for p in new if not p.get('partnerSkill'))
no_food = sum(1 for p in new if not p.get('food'))
print(f'No skills: {no_skills}')
print(f'No drops: {no_drops}')
print(f'No biomes: {no_biomes}')
print(f'No partner: {no_partner}')
print(f'No food: {no_food}')
