# -*- coding: utf-8 -*-
"""Fetch Fandom data for all 286 mapped pals, focusing on biomes + filling gaps."""
import urllib.request, json, urllib.parse, time, re

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json',
}

# Load
pals = json.load(open('src/data/pals.json', encoding='utf-8'))
mapping = json.load(open('scripts/slug-to-fandom-final.json', encoding='utf-8'))
db = json.load(open('scripts/raw-palcalc-db.json', encoding='utf-8'))

# Skill catalog lookup
catalog_by_name = {}
for s in db['ActiveSkills']:
    catalog_by_name[s['Name']] = s
    zh = s.get('LocalizedNames', {}).get('zh-Hans', '')
    if zh:
        catalog_by_name[zh] = s

ELEMENT_MAP = {
    'Normal': 'neutral', 'Fire': 'fire', 'Water': 'water', 'Grass': 'grass',
    'Electric': 'electric', 'Ice': 'ice', 'Ground': 'ground',
    'Dark': 'dark', 'Dragon': 'dragon',
}

def fetch_page(title, retries=2):
    enc = urllib.parse.quote(title)
    url = f'https://palworld.fandom.com/api.php?action=query&format=json&prop=revisions&titles={enc}&rvprop=content&rvslots=main&redirects=1'
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            r = urllib.request.urlopen(req, timeout=15)
            j = json.loads(r.read().decode('utf-8'))
            pages = j.get('query', {}).get('pages', {})
            for pid, p in pages.items():
                if int(pid) > 0:
                    revs = p.get('revisions', [])
                    if revs:
                        return p.get('title', title), revs[0]['slots']['main']['*']
            return title, None
        except Exception as e:
            if attempt < retries:
                time.sleep(1)
                continue
            return title, None
    return title, None

def parse_wiki(content):
    out = {'drops': [], 'partner_skill': None, 'active_skills': [], 'biomes': [], 'food': 0}
    if not content:
        return out
    m = re.search(r'\|\s*drops\s*=\s*([^\n]+)', content)
    if m:
        text = m.group(1)
        for part in re.split(r'<br\s*/?>', text)[:6]:
            for i in re.findall(r'\{\{i\|([^}]+)\}\}', part):
                if i.strip() and i.strip() not in out['drops']:
                    out['drops'].append(i.strip())
    m = re.search(r'\|\s*partnerskill\s*=\s*([^\n]+)', content)
    if m:
        nm = re.match(r'([^|{]+)', m.group(1).strip())
        if nm:
            out['partner_skill'] = nm.group(1).strip()
    m = re.search(r'===\s*Wild Spawn\s*===(.*?)(?====|\Z)', content, re.DOTALL)
    if m:
        for lm in re.finditer(r'\[\[([^\]|]+?)(?:\|[^\]]+)?\]\]', m.group(1)):
            b = lm.group(1).strip()
            if b and b not in out['biomes'] and not b.startswith('File:'):
                out['biomes'].append(b)
    m = re.search(r'==\s*Active Skills\s*==(.*?)(?====|\Z)', content, re.DOTALL)
    if m:
        for sm in re.finditer(r'\{\{PalSkillListEntry\+?\|([^|}]+)\|level=(\d+)\}\}', m.group(1)):
            out['active_skills'].append({'name': sm.group(1).strip(), 'level': int(sm.group(2))})
    m = re.search(r'\|\s*food\s*=\s*(\d+)', content)
    if m:
        out['food'] = int(m.group(1))
    return out

def slugify(s):
    return re.sub(r'[^a-zA-Z0-9]+', '-', s.lower()).strip('-')

def build_skill(skill_entry):
    name = skill_entry['name']
    level = skill_entry['level']
    cat = catalog_by_name.get(name, {})
    if not cat:
        clean = re.sub(r'\s*\([^)]+\)$', '', name)
        cat = catalog_by_name.get(clean, {})
    if not cat:
        return {
            'id': slugify(name), 'name': {'zh': name, 'en': name},
            'level': level, 'type': 'neutral', 'power': 0, 'cooldown': 0,
            'description': {'zh': '', 'en': ''},
        }
    element = ELEMENT_MAP.get(cat.get('ElementInternalName', 'Normal'), 'neutral')
    zh = cat.get('LocalizedNames', {}).get('zh-Hans', cat['Name'])
    return {
        'id': cat.get('InternalName', slugify(name)),
        'name': {'zh': zh, 'en': cat['Name']},
        'level': level, 'type': element,
        'power': cat.get('Power', 0), 'cooldown': int(cat.get('CooldownSeconds', 0)),
        'description': {'zh': '', 'en': ''},
    }

# Process pals missing data
to_process = [p for p in pals
              if not p.get('biomes') or not p.get('drops') or not p.get('skills') or p.get('food', 0) == 0
              and mapping.get(p['id'])]

print(f'Pals to process: {len(to_process)}')
print(f'  - of which with biomes mapping: {sum(1 for p in to_process if p["id"] in mapping)}')

updated = 0
skipped = 0
for i, pal in enumerate(to_process):
    title = mapping.get(pal['id'])
    if not title:
        skipped += 1
        continue
    actual_title, content = fetch_page(title)
    parsed = parse_wiki(content)
    # Apply
    if parsed['drops'] and not pal.get('drops'):
        pal['drops'] = parsed['drops']
    if parsed['biomes'] and not pal.get('biomes'):
        pal['biomes'] = parsed['biomes']
    if parsed['active_skills'] and not pal.get('skills'):
        pal['skills'] = [build_skill(s) for s in parsed['active_skills']]
    if parsed['food'] and (not pal.get('food') or pal['food'] == 0):
        pal['food'] = parsed['food']
    if parsed['partner_skill'] and not pal.get('partnerSkill'):
        pal['partnerSkill'] = {
            'id': slugify(parsed['partner_skill']),
            'name': {'zh': parsed['partner_skill'], 'en': parsed['partner_skill']},
            'description': {'zh': '', 'en': ''},
        }
    pal['updatedAt'] = '2026-07-28'
    updated += 1
    if (i + 1) % 20 == 0:
        print(f'  [{i+1}/{len(to_process)}] {pal["id"]:30s} biomes={len(pal["biomes"])} drops={len(pal["drops"])} skills={len(pal["skills"])}', flush=True)
    time.sleep(0.25)  # rate limit

print(f'\nUpdated: {updated}, Skipped: {skipped}')

# Save
json.dump(pals, open('src/data/pals.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('Saved pals.json')

# Final summary
still_missing = [p for p in pals
                 if not p.get('skills') or not p.get('drops') or not p.get('biomes')]
print(f'\nPals still missing data: {len(still_missing)}')
for p in still_missing[:30]:
    missing = []
    if not p.get('skills'): missing.append('skills')
    if not p.get('drops'): missing.append('drops')
    if not p.get('biomes'): missing.append('biomes')
    print(f"  {p['id']:30s} {missing}")
