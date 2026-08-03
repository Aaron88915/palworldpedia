#!/usr/bin/env python3
import json
import os

print('=== 数据缺口审计 ===\n')

# Tech descriptions
with open('src/data/tech.json', encoding='utf-8') as f:
    techs = json.load(f)
print(f'Tech 总数: {len(techs)}')
no_desc = [t for t in techs if not t.get('description') or len(t.get('description', '').strip()) < 30]
print(f'无/短 description: {len(no_desc)}')
print(f'已有 description: {len(techs) - len(no_desc)}')
print()
# 按 category
no_desc_struct = [t for t in no_desc if t['category'] == 'Structures']
no_desc_items = [t for t in no_desc if t['category'] == 'Items']
print(f'  Structures 缺: {len(no_desc_struct)}')
print(f'  Items 缺: {len(no_desc_items)}')
print()
print('前 20 个缺的（按 category/cost/name）:')
for t in no_desc[:20]:
    print(f'  [{t["category"][:3]}] Lv{t["cost"]} {t["slug"]}')
print()

# Pals biomes
with open('src/data/pals.json', encoding='utf-8') as f:
    pals = json.load(f)
print(f'Pals 总数: {len(pals)}')
no_biomes = [p for p in pals if not p.get('biomes') or len(p.get('biomes', [])) == 0]
print(f'无 biomes: {len(no_biomes)}')
no_biomes_base = [p for p in no_biomes if p.get('paldeckNo', 0) > 0 and p.get('paldeckNo', 0) < 200]
no_biomes_var = [p for p in no_biomes if p not in no_biomes_base]
print(f'  基础帕鲁缺: {len(no_biomes_base)}')
print(f'  变种帕鲁缺: {len(no_biomes_var)}')
print()
print('前 20 个缺 biomes 的:')
for p in no_biomes[:20]:
    print(f'  #{p["paldeckNo"]} {p["name"]["zh"]} ({p["name"]["en"]})')
