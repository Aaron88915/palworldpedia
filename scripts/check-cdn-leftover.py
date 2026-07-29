import json
with open('src/data/tech.json', 'r', encoding='utf-8') as f:
    techs = json.load(f)
still_cdn = [t for t in techs if t['icon'].startswith('https://cdn.paldb.cc/')]
print(f'Still CDN: {len(still_cdn)}')
for t in still_cdn:
    print(f'  {t["name"]} -> {t["icon"].split("/")[-1]}')
