# -*- coding: utf-8 -*-
"""Final pass: fill partner skill + try free-text biomes for ALL 286 mapped pals."""
import urllib.request, json, urllib.parse, time, re

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json',
}

pals = json.load(open('src/data/pals.json', encoding='utf-8'))
mapping = json.load(open('scripts/slug-to-fandom-final.json', encoding='utf-8'))

def fetch_page(title, retries=2):
    enc = urllib.parse.quote(title)
    url = f'https://palworld.fandom.com/api.php?action=query&format=json&prop=revisions&titles={enc}&rvprop=content&rvslots=main&redirects=1'
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            r = urllib.request.urlopen(req, timeout=20)
            j = json.loads(r.read().decode('utf-8'))
            pages = j.get('query', {}).get('pages', {})
            for pid, p in pages.items():
                if int(pid) > 0:
                    revs = p.get('revisions', [])
                    if revs:
                        return p.get('title', title), revs[0]['slots']['main']['*']
            return title, None
        except:
            if attempt < retries:
                time.sleep(2)
                continue
            return title, None
    return title, None

def parse_wiki(content):
    out = {'partner_skill': None, 'partner_skill_desc': None, 'biomes': []}
    if not content:
        return out
    # Partner skill name
    m = re.search(r'\|\s*partnerskill\s*=\s*([^\n]+)', content)
    if m:
        nm = re.match(r'([^|{]+)', m.group(1).strip())
        if nm:
            out['partner_skill'] = nm.group(1).strip()
    # Description
    m = re.search(r'\|\s*psdesc\s*=\s*([^\n]+)', content)
    if m:
        out['partner_skill_desc'] = m.group(1).strip()
    # Wild Spawn
    m = re.search(r'===\s*Wild Spawn\s*===(.*?)(?====|\Z)', content, re.DOTALL)
    if m:
        for lm in re.finditer(r'\[\[([^\]|]+?)(?:\|[^\]]+)?\]\]', m.group(1)):
            b = lm.group(1).strip()
            if b and b not in out['biomes'] and not b.startswith('File:'):
                out['biomes'].append(b)
    # Free-text "Near X" fallback
    if not out['biomes']:
        avail_m = re.search(r'==\s*Availability\s*==(.*?)==', content, re.DOTALL)
        if avail_m:
            text = avail_m.group(1)
            for nm in re.finditer(r'Near\s+([A-Z][A-Za-z\s\']+?)(?:,|\.|$)', text, re.MULTILINE):
                b = nm.group(1).strip()
                if b and b not in out['biomes'] and len(b) < 50:
                    out['biomes'].append(b)
    return out

def slugify(s):
    return re.sub(r'[^a-zA-Z0-9]+', '-', s.lower()).strip('-')

# Process: 44 missing partner + all still missing biomes
to_process = [p for p in pals if (not p.get('partnerSkill') or not p.get('biomes')) and p['id'] in mapping]
print(f'Pals to process: {len(to_process)}')

updated = 0
for i, pal in enumerate(to_process):
    title = mapping.get(pal['id'])
    actual_title, content = fetch_page(title)
    parsed = parse_wiki(content)
    if not pal.get('partnerSkill') and parsed['partner_skill']:
        pal['partnerSkill'] = {
            'id': slugify(parsed['partner_skill']),
            'name': {'zh': parsed['partner_skill'], 'en': parsed['partner_skill']},
            'description': {'zh': '', 'en': ''},
        }
        if parsed['partner_skill_desc']:
            pal['partnerSkill']['description']['en'] = parsed['partner_skill_desc']
    if not pal.get('biomes') and parsed['biomes']:
        pal['biomes'] = parsed['biomes']
    pal['updatedAt'] = '2026-07-28'
    updated += 1
    if (i + 1) % 30 == 0:
        print(f'  [{i+1}/{len(to_process)}] {pal["id"]:30s} partner={pal.get("partnerSkill") is not None} biomes={len(pal["biomes"])}', flush=True)
    time.sleep(0.25)

print(f'\nUpdated: {updated}')

json.dump(pals, open('src/data/pals.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('Saved')

# Final stats
print()
print('=== Final ===')
print(f'No skills: {sum(1 for p in pals if not p.get("skills"))}')
print(f'No drops: {sum(1 for p in pals if not p.get("drops"))}')
print(f'No biomes: {sum(1 for p in pals if not p.get("biomes"))}')
print(f'No partner: {sum(1 for p in pals if not p.get("partnerSkill"))}')
print(f'No food: {sum(1 for p in pals if not p.get("food"))}')
