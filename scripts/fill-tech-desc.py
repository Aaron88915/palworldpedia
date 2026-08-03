#!/usr/bin/env python3
"""
Fill missing tech descriptions in src/data/tech.json.

Sources (in priority order):
  1. paldb.cc/en/{slug} -- extract <meta property="og:description">
  2. scripts/wikigg-tech-data.json (match by name)
  3. Fallback generated from category + name + cost

Length target: 70-155 chars. Cap at 155 with "…".
"""
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TECH_JSON = ROOT / 'src' / 'data' / 'tech.json'
WIKI_JSON = ROOT / 'scripts' / 'wikigg-tech-data.json'
CACHE = ROOT / 'scripts' / 'paldb-tech-desc-cache.json'

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
BASE = "https://paldb.cc/en/"

MIN_LEN = 30
IDEAL_MAX = 155  # cap with ellipsis
SLEEP = 0.35     # seconds between paldb requests


def http_get(url, retries=2):
    """GET url, return (status, body). status is int or 0 on transport error."""
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept-Language': 'en'})
    last_err = 0
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                body = r.read()
                return r.status, body
        except urllib.error.HTTPError as e:
            return e.code, b''
        except Exception as e:
            last_err = -1
            if attempt < retries:
                time.sleep(0.8)
    return last_err, b''


def extract_og(html_bytes):
    """Extract og:description / meta description from HTML bytes."""
    try:
        html = html_bytes.decode('utf-8', errors='replace')
    except Exception:
        return ''
    # Try og:description first (most informative)
    m = re.search(
        r'<meta[^>]+property=["\']og:description["\'][^>]+content=["\']([^"\']+)["\']',
        html, re.I
    )
    if m:
        return unescape(m.group(1)).strip()
    # Fall back to <meta name="description">
    m = re.search(
        r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)["\']',
        html, re.I
    )
    if m:
        return unescape(m.group(1)).strip()
    return ''


def unescape(s):
    # Cheap HTML entity decode
    s = s.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    s = s.replace('&quot;', '"').replace('&#39;', "'").replace('&apos;', "'")
    s = s.replace('&nbsp;', ' ')
    return s


def build_candidates(tech):
    """Build a list of paldb URL slugs to try for this tech."""
    name = tech['name']
    slug = tech['slug']
    # Strip apostrophes (curly + straight) and commas
    name_clean = name.replace("'", '').replace('\u2019', '').replace(',', '').strip()
    name_under = name_clean.replace(' ', '_')
    name_under_dash = name_under.replace('-', '_')
    slug_clean = slug.replace("'", '').replace('\u2019', '').strip()
    slug_no_us = slug.replace('_', '')
    # Multiple words in name joined
    name_join = name_clean.replace(' ', '').replace('-', '').replace('_', '')
    # Try url-encoded apostrophe
    name_pct = name.replace("'", '%27').replace('\u2019', '%27').replace(' ', '_')

    candidates = []
    seen = set()
    for c in [
        name_under,           # Foxparks_Harness
        name_under_dash,      # same but with - → _
        name_pct,             # Foxparks%27_Harness
        slug_clean,           # original slug
        slug,                 # original
        slug_no_us,           # GuildChest
        name_clean,           # Foxparks Harness (with %20 ?)
        name_join,            # SingleShotSphereLauncher
    ]:
        if c and c not in seen:
            seen.add(c)
            candidates.append(c)
    return candidates


def try_paldb(tech, cache, log):
    """Try paldb.cc for description. Return (desc, source_url) or ('', '')."""
    cache_key = tech['slug']
    if cache_key in cache:
        entry = cache[cache_key]
        if entry.get('desc'):
            return entry['desc'], entry.get('url', '')
        if entry.get('failed'):
            return '', ''

    for cand in build_candidates(tech):
        url = BASE + urllib.parse.quote(cand, safe='_')
        status, body = http_get(url)
        if status == 200 and body:
            desc = extract_og(body)
            if desc and len(desc) >= 20:
                # Sanity: not a generic site description
                low = desc.lower()
                if 'paldb' in low and 'wiki' in low and 'database' in low and len(desc) < 60:
                    # generic site boilerplate, skip
                    pass
                else:
                    cache[cache_key] = {'desc': desc, 'url': url, 'cand': cand}
                    return desc, url
        # Don't hammer: short sleep
        time.sleep(SLEEP)
    cache[cache_key] = {'failed': True}
    return '', ''


def try_wiki(tech, wiki_by_name):
    """Try wiki.gg data by name match. Return desc or ''."""
    w = wiki_by_name.get(tech['name'].lower())
    if not w:
        return ''
    desc = (w.get('description') or '').strip()
    if not desc:
        return ''
    # wiki desc often has multiple lines / cost line appended; keep first paragraph
    first = desc.split('\n')[0].strip()
    return first


def make_fallback(tech):
    """Generate a fallback description for techs we couldn't fetch."""
    cat = tech['category']
    name = tech['name']
    cost = tech.get('cost', 0)
    lvl = f"Unlocks at level {cost}" if cost else "Always unlocked"
    if cat == 'Structures':
        # Detect furniture vs functional
        low = name.lower()
        if 'furniture' in low or 'set' in low or 'lamp' in low or 'chair' in low \
                or 'desk' in low or 'couch' in low or 'piano' in low or 'clock' in low \
                or 'carpet' in low or 'mirror' in low or 'barrel' in low or 'bath' in low \
                or 'planter' in low or 'sign' in low or 'fireplace' in low \
                or 'houseplant' in low or 'antiqu' in low or 'metal' in low \
                or 'ironwood' in low or 'leather' in low or 'outdoor' in low \
                or 'amusement' in low or 'street' in low or 'emergency' in low \
                or 'traffic' in low or 'road' in low or 'barricade' in low:
            return f"{name} is a decorative furniture set for base building. {lvl}. Place to customize your Palworld base interior."
        if 'chest' in low or 'storage' in low or 'palbox' in low or 'pod' in low or 'dispenser' in low:
            return f"{name} is a base storage and logistics structure. {lvl}. Stores and manages items in your Palworld base."
        if 'lab' in low or 'research' in low or 'monitor' in low:
            return f"{name} is a base research and production structure. {lvl}. Used to research and craft advanced Palworld tech."
        if 'refrigerator' in low or 'cooler' in low or 'heater' in low or 'lamp' in low or 'snowman' in low:
            return f"{name} is a utility structure for environmental control and base lighting. {lvl}. Helps maintain working conditions in your base."
        if 'gate' in low or 'door' in low or 'wall' in low or 'fence' in low or 'floor' in low or 'foundation' in low or 'stairs' in low or 'roof' in low or 'stair' in low:
            return f"{name} is a buildable base structure piece. {lvl}. Used to construct and protect your Palworld base layout."
        if 'crusher' in low or 'sawmill' in low or 'workbench' in low or 'assembly' in low or 'workshop' in low or 'factory' in low or 'silo' in low:
            return f"{name} is a production and crafting structure. {lvl}. Used to craft and process materials in your base."
        if 'altar' in low or 'shrine' in low:
            return f"{name} is a base shrine structure used for summoning bosses. {lvl}. Place to enable specific boss encounters in Palworld."
        if 'clinic' in low or 'medical' in low or 'pal_bed' in low or 'pal pod' in low:
            return f"{name} is a base medical and recovery structure. {lvl}. Heals and revives Pals in your base."
        # Generic structure
        return f"{name} is a buildable base structure. {lvl}. Used to expand and upgrade your Palworld base."
    else:  # Items
        low = name.lower()
        if 'arrow' in low:
            return f"{name} is a craftable ranged ammunition. {lvl}. Used with bows to deal elemental damage in combat."
        if 'harness' in low or 'saddle' in low:
            return f"{name} is a Pal equipment item that enables riding and saddle skills. {lvl}. Equip on a compatible Pal."
        if 'shotgun' in low or 'rifle' in low or 'launcher' in low or 'musket' in low or 'gun' in low or 'sphere launcher' in low:
            return f"{name} is a craftable ranged weapon. {lvl}. Used by the player for combat at range."
        if 'axe' in low or 'pickaxe' in low or 'shovel' in low or 'multicutter' in low or 'mining tool' in low:
            return f"{name} is a craftable gathering and mining tool. {lvl}. Used to chop wood, mine ore, and gather resources."
        if 'board' in low or 'wood' in low or 'ingot' in low or 'cement' in low or 'polymer' in low or 'cloth' in low or 'leather' in low or 'circuit' in low or 'battery' in low or 'nail' in low or 'stone' in low or 'material' in low:
            return f"{name} is a refined crafting material. {lvl}. Required for producing higher-tier items and structures."
        if 'holster' in low or 'inventory' in low or 'equipment slot' in low:
            return f"{name} is a player utility unlock. {lvl}. Expands your equipment or inventory capacity in Palworld."
        if 'ultrakill' in low or 'collab' in low:
            return f"{name} is a special collaboration cosmetic set. {lvl}. Unlock and equip to customize your Palworld look."
        # Generic item
        return f"{name} is a craftable item or unlock. {lvl}. Required materials and full stats available on the detail page."


def cap_desc(s, n=IDEAL_MAX):
    s = s.strip()
    # Collapse internal whitespace
    s = re.sub(r'\s+', ' ', s)
    # Remove trailing period before ellipsis to keep it tidy
    if len(s) > n:
        s = s[:n - 1].rstrip(' ,;:.-') + '\u2026'
    return s


def clean_desc(s):
    """Normalize a fetched description: remove trailing generic noise, ensure ends with period."""
    if not s:
        return ''
    s = re.sub(r'\s+', ' ', s).strip()
    # Strip redundant cost sentences like "It is a tier 34 ancient technology item and requires 4 ancient technology points to unlock."
    # (we'll add our own unlock info)
    # But keep such info if it has real content. For now, keep verbatim.
    # Ensure ends with punctuation
    if not s.endswith(('.', '!', '?', '\u2026')):
        s += '.'
    return s


def main():
    techs = json.loads(TECH_JSON.read_text(encoding='utf-8'))
    wiki = json.loads(WIKI_JSON.read_text(encoding='utf-8'))
    wiki_by_name = {w['name'].lower(): w for w in wiki if w.get('name')}

    # Load paldb cache
    cache = {}
    if CACHE.exists():
        try:
            cache = json.loads(CACHE.read_text(encoding='utf-8'))
        except Exception:
            cache = {}

    need = [t for t in techs
            if not t.get('description') or len(t.get('description', '').strip()) < MIN_LEN]
    print(f'[start] need to fill: {len(need)}')

    sources = {'paldb': 0, 'wiki': 0, 'fallback': 0, 'skipped': 0}
    log = []
    filled = []

    for i, t in enumerate(need, 1):
        # 1. paldb
        desc, url = try_paldb(t, cache, log)
        src = ''
        if desc:
            src = 'paldb'
        else:
            # 2. wiki by name
            wdesc = try_wiki(t, wiki_by_name)
            if wdesc:
                desc = wdesc
                src = 'wiki'
            else:
                # 3. fallback
                desc = make_fallback(t)
                src = 'fallback'

        # Clean / cap
        desc = clean_desc(desc)
        desc = cap_desc(desc, IDEAL_MAX)

        if len(desc.strip()) < MIN_LEN:
            # Should not happen given fallback, but guard
            desc = (desc + ' ' + 'Craftable Palworld tech with full stats and required materials.')[:IDEAL_MAX]
            desc = cap_desc(desc, IDEAL_MAX)
            if len(desc.strip()) < MIN_LEN:
                sources['skipped'] += 1
                continue

        t['description'] = desc
        sources[src] += 1
        filled.append((t['slug'], src, len(desc)))
        if i % 10 == 0:
            print(f'  [{i}/{len(need)}] last: {t["slug"]} via {src} ({len(desc)} chars)')

    # Save
    TECH_JSON.write_text(json.dumps(techs, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding='utf-8')

    print()
    print('=== Filled ===')
    print(f"  paldb:    {sources['paldb']}")
    print(f"  wiki:     {sources['wiki']}")
    print(f"  fallback: {sources['fallback']}")
    print(f"  skipped:  {sources['skipped']}")
    print(f"  total:    {sum(sources.values()) - sources['skipped']}")
    print()
    # Sample filled
    print('Sample filled (slug | source | chars | first 100):')
    for slug, src, n in filled[:10]:
        # find the tech
        rec = next((x for x in techs if x['slug'] == slug), None)
        if rec:
            print(f'  {slug:35} | {src:8} | {n:3} | {rec["description"][:100]}')


if __name__ == '__main__':
    main()
