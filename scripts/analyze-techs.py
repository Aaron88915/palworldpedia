import json
from collections import Counter
with open('scripts/raw-tech-list.json', 'r', encoding='utf-8') as f:
    techs = json.load(f)
print(f'Total techs: {len(techs)}')
c = Counter(t['category'] for t in techs)
print('By category:', dict(c))
c = Counter(t['cost'] for t in techs)
print('By cost:', dict(sorted(c.items())))
print()
print('Sample:')
for t in techs[:10]:
    print(f'  Lv{t["cost"]} [{t["category"]}] {t["name"]} -> {t["slug"]}')
