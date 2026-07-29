# -*- coding: utf-8 -*-
"""Fetch Fandom wiki content for 16 missing pals + sample biome-less ones."""
import urllib.request, json, urllib.parse, time, re

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json',
}

# Map slug -> Fandom page title (from earlier mapping - convert)
# Slug -> "Name Suffix" or just "Name"
# These are the 16 missing-all pals
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

# Also some pals that have skills but no biomes - get from a sample
BIOMES_SAMPLE = {
    'lamball': 'Lamball',
    'cattiva': 'Cattiva',
    'chikipi': 'Chikipi',
    'lifmunk': 'Lifmunk',
    'hoocrates': 'Hoocrates',
    'pengullet': 'Pengullet',
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
                return revs[0]['slots']['main']['*']
    return None

def parse_wiki(content):
    """Extract drops, partnerSkill, and any active skills from Fandom wikitext."""
    out = {'drops': [], 'partner_skill': None, 'active_skills': [], 'biomes': []}
    if not content:
        return out
    # Drops
    m = re.search(r'\|\s*drops\s*=\s*([^\n]+)', content)
    if m:
        text = m.group(1)
        # Extract item names from {{i|ItemName}}
        items = re.findall(r'\{\{i\|([^}]+)\}\}', text)
        # Also handle plain names
        for i in items:
            out['drops'].append(i.strip())
    # Partner skill
    m = re.search(r'\|\s*partnerskill\s*=\s*([^\n]+)', content)
    if m:
        out['partner_skill'] = m.group(1).strip()
    # Biomes (look in the gallery section or in 'habitat' field)
    m = re.search(r'\|\s*habitat\s*=\s*([^\n]+)', content)
    if m:
        text = m.group(1)
        biomes = re.findall(r'\[\[([^]|]+?)(?:\|[^\]]+)?\]\]', text)
        out['biomes'] = [b.strip() for b in biomes]
    return out

print('=== Fetching 16 missing-all pals ===\n')
results = {}
for slug, title in PAL_TITLE_MAP.items():
    print(f'Fetching {title}...', end=' ', flush=True)
    try:
        content = fetch_page(title)
        parsed = parse_wiki(content)
        results[slug] = parsed
        print(f'drops={len(parsed["drops"])} partner={parsed["partner_skill"][:30] if parsed["partner_skill"] else None}')
    except Exception as e:
        print(f'ERR: {e}')
    time.sleep(0.3)

print('\n=== Sample biome-less pals ===\n')
for slug, title in BIOMES_SAMPLE.items():
    print(f'Fetching {title}...', end=' ', flush=True)
    try:
        content = fetch_page(title)
        parsed = parse_wiki(content)
        print(f'drops={parsed["drops"]} biomes={parsed["biomes"]}')
    except Exception as e:
        print(f'ERR: {e}')
    time.sleep(0.3)

# Save raw parsed data
json.dump(results, open('scripts/fandom-missing-pals.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('\nSaved to scripts/fandom-missing-pals.json')
