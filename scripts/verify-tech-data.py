import json

with open('src/data/tech.json', 'r', encoding='utf-8') as f:
    techs = json.load(f)
with open('scripts/raw-tech-list.json', 'r', encoding='utf-8') as f:
    paldb_list = json.load(f)
with open('scripts/gg-tech-icon-map.json', 'r', encoding='utf-8') as f:
    gg_map = json.load(f)

# Build a dict
tech_by_id = {t['id']: t for t in techs}
paldb_by_name = {t['name']: t for t in paldb_list}

# 24 in palworld.gg not in ours - check if they're really tech or items
gg_only = sorted(set(gg_map.keys()) - {t['name'] for t in techs})
print(f'24 names in palworld.gg tech-tree but not in our tech list:')
for n in gg_only:
    print(f'  {n}')

# Check if any of those 24 exist on paldb.cc under a different name
print(f'\nLooking for paldb.cc matches...')
paldb_all_names = list(paldb_by_name.keys())
for gg_name in gg_only:
    # Try exact match
    if gg_name in paldb_by_name:
        continue
    # Try matching last word (e.g. 'Saddled Harness' from 'Direhowl's Saddled Harness')
    words = gg_name.split()
    if len(words) > 1:
        for w in words[1:]:
            if w in paldb_all_names:
                print(f'  {gg_name!r} -> {w!r}')
                break

# Check our techs that have very short names that might be wrong
print(f'\n=== Suspicious techs in our data ===')
suspicious = [t for t in techs if len(t['name']) < 3 or t['name'].isdigit()]
print(f'Very short or numeric: {len(suspicious)}')
for t in suspicious[:10]:
    print(f'  {t["name"]!r} -> slug={t["slug"]!r}')

# Techs with cost 6+ (unusual)
print(f'\n=== High-cost techs (Lv 6+) ===')
for t in techs:
    if t['cost'] >= 6:
        print(f'  Lv{t["cost"]} {t["name"]} ({t["category"]})')

# Check for duplicate slugs
print(f'\n=== Duplicate slugs ===')
slugs = {}
for t in techs:
    s = t['slug']
    slugs.setdefault(s, []).append(t['name'])
dups = {s: names for s, names in slugs.items() if len(names) > 1}
print(f'Duplicate slugs: {len(dups)}')
for s, names in dups.items():
    print(f'  {s}: {names}')

# Verify level consistency: Lv 1 should be basic, Lv 5+ should be advanced
print(f'\n=== Stats overview ===')
from collections import Counter
print(f'Category distribution: {Counter(t["category"] for t in techs)}')
print(f'Cost distribution: {dict(sorted(Counter(t["cost"] for t in techs).items()))}')
print(f'Techs with materials: {sum(1 for t in techs if t.get("materials"))}')
print(f'Techs with description: {sum(1 for t in techs if t.get("description"))}')
print(f'Techs with product != name: {sum(1 for t in techs if t.get("product") and t["product"] != t["name"])}')
