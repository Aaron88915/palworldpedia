import json
with open('src/data/tech.json', 'r', encoding='utf-8') as f:
    techs = json.load(f)
missing = [t for t in techs if t['icon'].startswith('https://cdn.paldb.cc/')]
print(f'Missing local: {len(missing)}')
for t in missing[:20]:
    print(f'  {t["name"]} -> {t["icon"].split("/")[-1]}')
