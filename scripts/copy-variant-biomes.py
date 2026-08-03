#!/usr/bin/env python3
"""为变种帕鲁复制基础帕鲁的 biomes"""
import json, re

pals = json.load(open('src/data/pals.json', encoding='utf-8'))

# 找变种（paldeckNo == 0 或 > 200）
variants = [p for p in pals if p.get('paldeckNo', 0) == 0 or p.get('paldeckNo', 0) > 200]
print(f'变种帕鲁总数: {len(variants)}')

# 找基础帕鲁：paldeckNo 在 1-200
base = {p['id']: p for p in pals if 0 < p.get('paldeckNo', 0) < 200}

def find_base_id(variant_id):
    """从变种 id 找基础 id（去掉 _Dark/_Ice/_Fire 等后缀）"""
    suffixes = [
        '_Dark', '_Ice', '_Fire', '_Electric', '_Grass', '_Ground', '_Dragon',
        '_Water', '_Blaze', '_Astral', '_Aqua', '_Special', '_Jelly',
        '_Stream', '_Alpine', '_Forest', '_Obsidian', '_Crystal', '_Fantasm',
        '_Storm', '_Shadow', '_Stone', '_King', '_Royal', '_Air', '_Emperor',
        '_Observer', '_Lovely', '_Crusher', '_Blockhead', '_Libero', '_Umbral',
        '_Master', '_Ryu', '_Primo',
    ]
    for s in suffixes:
        if variant_id.endswith(s):
            base_id = variant_id[:-len(s)]
            if base_id in base:
                return base_id
    return None

# 复制
fixed = 0
unfixed = []
for v in variants:
    if v.get('biomes'):
        continue
    bid = find_base_id(v['id'])
    if bid and base[bid].get('biomes'):
        v['biomes'] = base[bid]['biomes']
        fixed += 1
        print(f'  {v["id"]} <- {bid}: {v["biomes"]}')
    else:
        unfixed.append(v['id'])

print(f'\n复制完成: {fixed}')
print(f'未找到基础: {len(unfixed)}')
for u in unfixed:
    print(f'  {u}')

# 写回
if fixed:
    json.dump(pals, open('src/data/pals.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print(f'\n已写回 pals.json (修复 {fixed} 个)')
