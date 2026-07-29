# -*- coding: utf-8 -*-
"""Match Fandom skill names with palcalc's ActiveSkills catalog to get types."""
import json

db = json.load(open('scripts/raw-palcalc-db.json', encoding='utf-8'))
skills_catalog = db['ActiveSkills']
# Build lookup: English name -> skill data
catalog_by_name = {}
for s in skills_catalog:
    name = s['Name']
    zh = s.get('LocalizedNames', {}).get('zh-Hans', '')
    catalog_by_name[name] = s
    if zh:
        catalog_by_name[zh] = s

print(f'palcalc catalog: {len(skills_catalog)} skills, indexed {len(catalog_by_name)}')
print('Sample keys:', list(catalog_by_name.keys())[:10])
print()

# Show what fields each skill has
sample = skills_catalog[0]
print('Sample skill fields:', list(sample.keys()))
print(json.dumps(sample, ensure_ascii=False, indent=2)[:800])
