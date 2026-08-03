#!/usr/bin/env python3
import json
print('=== DATA GAP AUDIT ===\n')

# Tech descriptions
with open('src/data/tech.json', encoding='utf-8') as f:
    techs = json.load(f)
print(f'Tech total: {len(techs)}')
no_desc = [t for t in techs if not t.get('description') or len(t.get('description', '').strip()) < 30]
print(f'Missing/short description: {len(no_desc)}')
print(f'Already filled: {len(techs) - len(no_desc)}')
print()
# By category
no_desc_struct = [t for t in no_desc if t['category'] == 'Structures']
no_desc_items = [t for t in no_desc if t['category'] == 'Items']
print(f'  Structures missing: {len(no_desc_struct)}')
print(f'  Items missing: {len(no_desc_items)}')
print()
print('Length distribution:')
def desc(t): return (t.get('description') or '').strip()
print(f'  <30 chars: {sum(1 for t in techs if len(desc(t)) < 30)}')
print(f'  30-70 chars: {sum(1 for t in techs if 0 < len(desc(t)) < 70)}')
print(f'  70-155 chars (SEO ideal): {sum(1 for t in techs if 70 <= len(desc(t)) <= 155)}')
print(f'  155-200 chars: {sum(1 for t in techs if 155 < len(desc(t)) < 200)}')
print(f'  >=200 chars: {sum(1 for t in techs if len(desc(t)) >= 200)}')
print()

# Pals biomes
with open('src/data/pals.json', encoding='utf-8') as f:
    pals = json.load(f)
print(f'Pals total: {len(pals)}')
no_biomes = [p for p in pals if not p.get('biomes') or len(p.get('biomes', [])) == 0]
print(f'No biomes: {len(no_biomes)}')
no_biomes_base = [p for p in no_biomes if p.get('paldeckNo', 0) > 0 and p.get('paldeckNo', 0) < 200]
no_biomes_var = [p for p in no_biomes if p not in no_biomes_base]
print(f'  Base pals missing: {len(no_biomes_base)}')
print(f'  Variant pals missing: {len(no_biomes_var)}')
