"""
Merge wikigg-tech-data.json into tech.json
"""
import json

with open('src/data/tech.json', 'r', encoding='utf-8') as f:
    techs = json.load(f)
with open('scripts/wikigg-tech-data.json', 'r', encoding='utf-8') as f:
    wikigg = json.load(f)

# Build slug -> wikigg data map
wikigg_by_slug = {r['slug']: r for r in wikigg if r.get('slug')}

# Also try matching by name (for cases where slug format differs)
wikigg_by_name = {r.get('name', ''): r for r in wikigg if r.get('name')}

print(f'Techs: {len(techs)}')
print(f'Wikigg entries: {len(wikigg)}')
print(f'Wikigg by slug: {len(wikigg_by_slug)}')

# Stats before
before_desc = sum(1 for t in techs if t.get('description'))
before_mat = sum(1 for t in techs if t.get('materials'))
print(f'\nBefore: {before_desc} desc, {before_mat} mats')

# Merge
merged_desc = 0
merged_mat = 0
merged_cost = 0
merged_lv = 0
no_match = []

for t in techs:
    w = wikigg_by_slug.get(t['slug']) or wikigg_by_name.get(t['name'])
    if not w:
        no_match.append(t['slug'])
        continue
    if w.get('description') and not t.get('description'):
        t['description'] = w['description']
        merged_desc += 1
    elif w.get('description') and len(w['description']) > len(t.get('description', '')):
        t['description'] = w['description']
        merged_desc += 1
    if w.get('materials') and not t.get('materials'):
        t['materials'] = w['materials']
        merged_mat += 1
    elif w.get('materials') and len(w['materials']) > len(t.get('materials', [])):
        t['materials'] = w['materials']
        merged_mat += 1
    if w.get('cost') is not None and t.get('cost') is None:
        t['cost'] = w['cost']
        merged_cost += 1
    if w.get('unlockLevel') is not None and t.get('unlockLevel') is None:
        t['unlockLevel'] = w['unlockLevel']
        merged_lv += 1

# Save
with open('src/data/tech.json', 'w', encoding='utf-8') as f:
    json.dump(techs, f, ensure_ascii=False, indent=1)

# Stats after
after_desc = sum(1 for t in techs if t.get('description'))
after_mat = sum(1 for t in techs if t.get('materials'))
print(f'\nMerged: {merged_desc} desc, {merged_mat} mats, {merged_cost} cost, {merged_lv} lv')
print(f'After: {after_desc} desc, {after_mat} mats')
print(f'\nUnmatched slugs: {len(no_match)}')
for s in no_match[:10]:
    print(f'  {s}')
