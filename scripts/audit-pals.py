# -*- coding: utf-8 -*-
import json

pals = json.load(open('src/data/pals.json', encoding='utf-8'))

# Identify pals missing data
no_skills = [p for p in pals if len(p.get('skills', [])) == 0]
no_drops = [p for p in pals if len(p.get('drops', [])) == 0]
no_biomes = [p for p in pals if len(p.get('biomes', [])) == 0]
no_partner = [p for p in pals if p.get('partnerSkill') is None]

print(f'Total pals: {len(pals)}')
print(f'No skills: {len(no_skills)}')
print(f'No drops: {len(no_drops)}')
print(f'No biomes: {len(no_biomes)}')
print(f'No partner skill: {len(no_partner)}')
print()

# Pals missing ALL three
missing_all = [p for p in pals
               if len(p.get('skills', [])) == 0
               and len(p.get('drops', [])) == 0
               and len(p.get('biomes', [])) == 0]
print(f'Missing all (skills+drops+biomes): {len(missing_all)}')
for p in missing_all[:30]:
    print(f"  {p['id']:30s} | {p.get('name',{}).get('en','?'):30s} | deckNo={p.get('paldeckNo', 0)}")
print()

# Pals missing just drops+biomes (have skills)
missing_drops_biomes = [p for p in pals
                        if len(p.get('skills', [])) > 0
                        and len(p.get('drops', [])) == 0
                        and len(p.get('biomes', [])) == 0]
print(f'Have skills but missing drops+biomes: {len(missing_drops_biomes)}')
for p in missing_drops_biomes[:30]:
    print(f"  {p['id']:30s} | {p.get('name',{}).get('en','?'):30s} | deckNo={p.get('paldeckNo', 0)}")
