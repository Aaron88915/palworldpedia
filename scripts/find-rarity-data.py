# -*- coding: utf-8 -*-
"""Find which JSON files have rarity data."""
import json, os

for f in sorted(os.listdir('scripts')):
    if not f.endswith('.json'):
        continue
    path = os.path.join('scripts', f)
    size = os.path.getsize(path)
    if size < 500:
        continue
    try:
        with open(path, 'r', encoding='utf-8') as fp:
            data = json.load(fp)
        # Look for keys that suggest rarity info
        rarity_count = 0
        sample_rarity = None
        if isinstance(data, dict):
            for k, v in data.items():
                if 'rarity' in str(k).lower():
                    rarity_count += 1
                    sample_rarity = v if isinstance(v, (str, int)) else str(v)[:50]
        elif isinstance(data, list) and data and isinstance(data[0], dict):
            for p in data:
                if 'rarity' in p:
                    rarity_count += 1
                    if not sample_rarity:
                        sample_rarity = p['rarity']
        if rarity_count > 0:
            print(f'{f}: rarity entries={rarity_count}, sample={sample_rarity}')
    except Exception as e:
        pass
