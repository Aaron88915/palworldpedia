#!/usr/bin/env python3
import json
pals = json.load(open('src/data/pals.json', encoding='utf-8'))
all_biomes = set()
for p in pals:
    for b in p.get('biomes', []):
        all_biomes.add(b)
print('=== 现存 biomes 集合 ===')
for b in sorted(all_biomes):
    print(f'  {b}')

# 看看哪些 pals 有 biomes
have = sum(1 for p in pals if p.get('biomes'))
print(f'\n有 biomes 的: {have} / {len(pals)}')

# 看一个有 biomes 的样本
for p in pals[:50]:
    if p.get('biomes'):
        print(f'\n样本: {p["name"]["zh"]} ({p["name"]["en"]})')
        print(f'  biomes: {p["biomes"]}')
        break
