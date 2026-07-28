# -*- coding: utf-8 -*-
"""Fetch and parse Fandom wiki content for the 16 missing-all pals."""
import urllib.request, json, urllib.parse, time, re

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json',
}

PAL_TITLE_MAP = {
    'gumoss-special': 'Gumoss',
    'fuack': 'Fuack',
    'celaray-lux': 'Celaray Lux',
    'pupperai': 'Pupperai',
    'clovee': 'Clovee',
    'tanzee': 'Tanzee',
    'rooby': 'Rooby',
    'foxparks-cryst': 'Foxparks Cryst',
    'caprity-noct': 'Caprity Noct',
    'sparkit': 'Sparkit',
    'loupmoon-cryst': 'Loupmoon Cryst',
    'fenglope-lux': 'Fenglope Lux',
    'dazzi-noct': 'Dazzi Noct',
    'dumud-gild': 'Dumud Gild',
    'kitsun-noct': 'Kitsun Noct',
    'cryolinx-terra': 'Cryolinx Terra',
}

def fetch_page(title):
    enc = urllib.parse.quote(title)
    url = f'https://palworld.fandom.com/api.php?action=query&format=json&prop=revisions&titles={enc}&rvprop=content&rvslots=main&redirects=1'
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

def parse_wiki(title, content):
    out = {
        'title': title,
        'drops': [],
        'partner_skill': None,
        'partner_skill_desc': None,
        'active_skills': [],  # List of {name, level, type}
        'biomes': [],
        'food': 0,
    }
    if not content:
        return out
    # Drops
    m = re.search(r'\|\s*drops\s*=\s*([^\n]+)', content)
    if m:
        text = m.group(1)
        # Remove anything after second "<br/>"
        parts = re.split(r'<br\s*/?>', text)
        for part in parts[:6]:  # up to 6 drops
            items = re.findall(r'\{\{i\|([^}]+)\}\}', part)
            for i in items:
                if i.strip() and i.strip() not in out['drops']:
                    out['drops'].append(i.strip())
    # Partner skill
    m = re.search(r'\|\s*partnerskill\s*=\s*([^\n]+)', content)
    if m:
        # Remove template markup
        ps = m.group(1).strip()
        # Could be "Name|icon=...|desc=..."
        # Take just the name part (before | or {{)
        name_match = re.match(r'([^|{]+)', ps)
        if name_match:
            out['partner_skill'] = name_match.group(1).strip()
        else:
            out['partner_skill'] = ps
    # Wild Spawn -> biomes
    m = re.search(r'===\s*Wild Spawn\s*===(.*?)(?====|\Z)', content, re.DOTALL)
    if m:
        text = m.group(1)
        for lm in re.finditer(r'\[\[([^\]|]+?)(?:\|[^\]]+)?\]\]', text):
            b = lm.group(1).strip()
            if b and b not in out['biomes'] and not b.startswith('File:'):
                out['biomes'].append(b)
    # Active Skills section (format: {{PalSkillListEntry+|Name|level=N}})
    m = re.search(r'==\s*Active Skills\s*==(.*?)(?====|\Z)', content, re.DOTALL)
    if m:
        text = m.group(1)
        for sm in re.finditer(r'\{\{PalSkillListEntry\+?\|([^|}]+)\|level=(\d+)\}\}', text):
            out['active_skills'].append({
                'name': sm.group(1).strip(),
                'level': int(sm.group(2)),
            })
    # Food
    m = re.search(r'\|\s*food\s*=\s*(\d+)', content)
    if m:
        out['food'] = int(m.group(1))
    return out

results = {}
for slug, title in PAL_TITLE_MAP.items():
    print(f'Fetching {title}...', end=' ', flush=True)
    try:
        actual_title, content = fetch_page(title)
        parsed = parse_wiki(actual_title, content)
        results[slug] = parsed
        print(f'drops={len(parsed["drops"])} partner={parsed["partner_skill"][:25] if parsed["partner_skill"] else "-"} biomes={len(parsed["biomes"])} skills={len(parsed["active_skills"])} food={parsed["food"]}')
    except Exception as e:
        print(f'ERR: {e}')
    time.sleep(0.3)

# Save
json.dump(results, open('scripts/fandom-missing-pals-v2.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('\nSaved to scripts/fandom-missing-pals-v2.json')
print()
# Detail
for slug, r in results.items():
    print(f'--- {slug} ---')
    print(f'  drops: {r["drops"]}')
    print(f'  partner: {r["partner_skill"]}')
    print(f'  biomes: {r["biomes"]}')
    print(f'  skills: {r["active_skills"]}')
    print(f'  food: {r["food"]}')
