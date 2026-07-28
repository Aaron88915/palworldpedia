# -*- coding: utf-8 -*-
"""Regenerate public/pals-data.json with breedRank + rarityTier + breedPower."""
import json

src = json.load(open('src/data/pals.json', encoding='utf-8'))
out = []
for p in src:
    out.append({
        'id': p['id'],
        'zh': p['name']['zh'],
        'en': p['name']['en'],
        'types': p.get('types', []),
        'img': p.get('image', ''),
        'rarity': p.get('rarity', 1),
        'rarityTier': p.get('rarityTier', 'Common'),
        'breedRank': p.get('breedRank', 0),
        'breedPower': p.get('breedPower', 0) or p.get('breedpower', 0),
        'partner': (p.get('partnerSkill') or {}).get('name', {}).get('zh', '') if isinstance(p.get('partnerSkill'), dict) else '',
        'passives': [ps.get('name', {}).get('zh', '') for ps in p.get('passives', [])] if isinstance(p.get('passives'), list) else [],
    })

with open('public/pals-data.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=0)

import os
size = os.path.getsize('public/pals-data.json')
print(f'Saved {len(out)} pals, size={size} bytes ({size/1024:.1f} KB)')

# Show a sample
print('\nSample (Jetragon):')
jet = next(p for p in out if p['id'] == 'jetragon')
print(json.dumps(jet, ensure_ascii=False, indent=2))
print('\nSample (Lamball):')
lam = next(p for p in out if p['id'] == 'lamball')
print(json.dumps(lam, ensure_ascii=False, indent=2))
