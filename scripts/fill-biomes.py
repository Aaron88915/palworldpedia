#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fill-biomes.py - Fill missing biomes for pals.json.

Strategy (in order, per missing pal):
  1. Hardcoded biomes for 5 special pals (paldeckNo 0 / 201+ / explicit names).
  2. Variant pals: copy biomes from base pal, but ONLY if the base's biomes
     are all in the standard English list (skip if base has Chinese or empty).
  3. Everyone still missing: fetch paldb.cc/en/{Name} and parse Pal Recruiter /
     zone / spawner / location data.  Map internal IDs to standard names.
  4. Still empty after paldb.cc: leave [] (the user said this is fine - don't fake).

Standard biome names (canonical list, in English):
  Windswept Island, Sea Breeze Archipelago, Marsh Island, Eastern Wild Island,
  Isle of Murmurs, Isle of Silence, Bamboo Groves, Twilight Dunes, Astral Mountains,
  Mount Obsidian, Sakurajima, Feybreak, Wildlife Sanctuary,
  No. 1/2/3 Wildlife Sanctuary, Sealed Realms, Dungeons, Alpha Pals, Enemies,
  Rampaging, Tower, Palpagos Islands

Run:  py scripts/fill-biomes.py
Output: writes src/data/pals.json, prints a report to stdout.
"""
import json
import os
import re
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

PALS_JSON = 'src/data/pals.json'
CACHE_DIR = 'scripts/_paldb_cache'
REPORT_FILE = 'scripts/fill-biomes-report.txt'
USER_AGENT = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
              '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

# --- Canonical biome list ----------------------------------------------------
STANDARD_BIOMES = {
    'Windswept Island',
    'Sea Breeze Archipelago',
    'Marsh Island',
    'Eastern Wild Island',
    'Isle of Murmurs',
    'Isle of Silence',
    'Bamboo Groves',
    'Twilight Dunes',
    'Astral Mountains',
    'Mount Obsidian',
    'Sakurajima',
    'Feybreak',
    'Wildlife Sanctuary',
    'No. 1 Wildlife Sanctuary',
    'No. 2 Wildlife Sanctuary',
    'No. 3 Wildlife Sanctuary',
    'Sealed Realms',
    'Dungeons',
    'Alpha Pals',
    'Enemies',
    'Rampaging',
    'Tower',
    'Palpagos Islands',
}

# --- Hardcoded biomes for the 5 special pals --------------------------------
# These are unique IDs that don't appear on paldb.cc with normal spawn rules.
# Sources: Palworld 1.0 wiki / community knowledge.
SPECIAL_BIOMES = {
    # green-slime = wild grass slime, no real spawn; lives in forest / grass areas
    'green-slime': ['Windswept Island', 'Marsh Island', 'Eastern Wild Island'],
    # gumoss-special is a dungeon / farm variant
    'gumoss-special': ['Dungeons'],
    # neptilius (paldeckNo 201) is a water legendary
    'neptilius': ['Sea Breeze Archipelago', 'Palpagos Islands'],
    # jetragon (paldeckNo 202) is the dragon legendary, Mount Obsidian sky
    'jetragon': ['Mount Obsidian', 'Wildlife Sanctuary'],
    # panthalus (paldeckNo 203) is the water legendary
    'panthalus': ['Sea Breeze Archipelago', 'Palpagos Islands'],
}

# --- paldb.cc internal biome ID -> standard name -----------------------------
PALDB_BIOME_ID_MAP = {
    'Forest_Volcano': 'Mount Obsidian',
    'DarkIsland':     'Isle of Silence',
    'Desert_Snow':    'Astral Mountains',
    'Grass':          'Marsh Island',   # generic grass plateau / eastern wild
    'Sakurajima':     'Sakurajima',
    'SkyIsland':      'Sea Breeze Archipelago',
    'MoonIsle':       'Isle of Murmurs',
}

# paldb.cc spawner / zone prefix -> standard biome
ZONE_PREFIX_MAP = {
    'grass':      'Marsh Island',
    'forest':     'Windswept Island',
    'desert':     'Twilight Dunes',
    'dessert':    'Twilight Dunes',  # typo in paldb.cc data
    'snow':       'Astral Mountains',
    'volcano':    'Mount Obsidian',
    'dark':       'Isle of Silence',
    'sky':        'Sea Breeze Archipelago',
    'moon':       'Isle of Murmurs',
    'feybreak':   'Feybreak',
    'sakurajima': 'Sakurajima',
    'sanctuary':  'Wildlife Sanctuary',
    'tropical':   'Windswept Island',
    'island':     'Windswept Island',
    'yellow':     'Marsh Island',
}

# paldb.cc spawner area (first word of the value) -> standard biome
# e.g. spawner=worldtree_9_55_WorldTreeAura -> 'worldtree' -> Sealed Realms
SPAWNER_AREA_MAP = {
    'worldtree':       'Sealed Realms',
    'skyisland':       'Sea Breeze Archipelago',
    'yamijima':        'Sakurajima',
    'Yamijima':        'Sakurajima',
    'sakura':          'Sakurajima',
    'sanctuary':       'Wildlife Sanctuary',
    'remainsIsland':   'Feybreak',  # Nitemary_Botan is a Feybreak pal
    'volcanoiskand':   'Mount Obsidian',  # typo: should be volcanoisland
    'Ocean':           'Sea Breeze Archipelago',
    'island':          'Windswept Island',
    'allarea':         'Palpagos Islands',  # generic, but treat as Palpagos
}

# specific named locations -> standard biome
LOCATION_BIOME_MAP = {
    'Astral_Mountains_Cavern':    'Astral Mountains',
    'Mount_Obsidian_Cavern':      'Mount Obsidian',
    'Palpagos_Islands':           'Palpagos Islands',
    'The_World_Tree':             'Sealed Realms',
    'World_Tree':                 'Sealed Realms',
    'Sealed_Realm':               'Sealed Realms',
    'IncidentSpawner_Snow':       'Astral Mountains',
    'IncidentSpawner_Volcano':    'Mount Obsidian',
    'IncidentSpawner_Grass':      'Marsh Island',
    'IncidentSpawner_Dark':       'Isle of Silence',
    'Wildlife_Sanctuary':         'Wildlife Sanctuary',
    'No_1_Wildlife_Sanctuary':    'No. 1 Wildlife Sanctuary',
    'No_2_Wildlife_Sanctuary':    'No. 2 Wildlife Sanctuary',
    'No_3_Wildlife_Sanctuary':    'No. 3 Wildlife Sanctuary',
}

# Chinese biome name (from the older fetch script) -> standard English
# Used to copy biomes from a base pal whose biomes are still in Chinese.
CHINESE_BIOME_MAP = {
    '\u4e91\u6d77\u5c9b':     'Sea Breeze Archipelago',  # 云海岛
    '\u6697\u6708\u5c9b':     'Isle of Silence',         # 暗月岛
    '\u6a31\u5c9b':           'Sakurajima',              # 樱岛
    '\u706b\u5c71\u6797':     'Mount Obsidian',          # 火山林
    '\u8349\u539f':           'Eastern Wild Island',     # 草原
    '\u96ea\u539f':           'Astral Mountains',        # 雪原
}

# --- Variant suffix list (lowercase, matched against id after last '-') ------
VARIANT_SUFFIXES = {
    'dark', 'ice', 'fire', 'electric', 'grass', 'ground', 'dragon',
    'water', 'blaze', 'astral', 'aqua', 'special', 'jelly',
    'stream', 'alpine', 'forest', 'obsidian', 'crystal', 'fantasm',
    'storm', 'shadow', 'stone', 'king', 'royal', 'air', 'emperor',
    'observer', 'lovely', 'crusher', 'blockhead', 'libero', 'umbral',
    'master', 'ryu', 'primo',
    'terra', 'cryst', 'ignis', 'lux', 'noct', 'botan', 'gild', 'hydro',
}

# --- Helpers -----------------------------------------------------------------
def slug_to_paldb_name(slug):
    """Convert internal pal slug to paldb.cc URL slug.

    paldb.cc uses Name_Suffix (underscore) for variants and Name for base.
    So 'fuack-ignis' -> 'Fuack_Ignis', 'lamball' -> 'Lamball'.
    """
    parts = slug.split('-')
    return '_'.join(p.capitalize() for p in parts)


def split_base_variant(pid):
    """Return (is_variant, base_id) for a pal id."""
    if '-' not in pid:
        return False, None
    suffix = pid.rsplit('-', 1)[-1]
    if suffix in VARIANT_SUFFIXES:
        return True, pid.rsplit('-', 1)[0]
    return False, None


def fetch_paldb(paldb_name, retries=1):
    """Fetch paldb.cc/en/{Name}, cache to disk. Return html or None.

    paldb_name should already be in the form 'Name' or 'Name_Suffix' (underscore).
    """
    cache_path = os.path.join(CACHE_DIR, paldb_name + '.html')
    if os.path.exists(cache_path) and os.path.getsize(cache_path) > 1000:
        try:
            return open(cache_path, encoding='utf-8', errors='ignore').read()
        except Exception:
            pass
    url = 'https://paldb.cc/en/' + paldb_name
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
            r = urllib.request.urlopen(req, timeout=25)
            html = r.read().decode('utf-8', errors='ignore')
            os.makedirs(CACHE_DIR, exist_ok=True)
            with open(cache_path, 'w', encoding='utf-8', errors='ignore') as f:
                f.write(html)
            return html
        except Exception:
            if attempt < retries:
                time.sleep(1.5)
            else:
                return None
    return None


def fetch_paldb_parallel(paldb_names, max_workers=6):
    """Fetch multiple paldb.cc pages in parallel. Returns dict name -> html."""
    results = {}
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        future_to_name = {pool.submit(fetch_paldb, n): n for n in paldb_names}
        for fut in as_completed(future_to_name):
            n = future_to_name[fut]
            try:
                results[n] = fut.result()
            except Exception:
                results[n] = None
    return results


def parse_biomes_from_paldb(html):
    """Extract a list of standard biome names from a paldb.cc HTML page.

    Sources (in order of reliability):
      1. 'Pal Recruiter: <BiomeId>' rows  -> map via PALDB_BIOME_ID_MAP
      2. 'zone=<zone>_grade_N' links       -> map by ZONE_PREFIX_MAP
      3. 'spawner=<zone>_*' links          -> same prefix map
      4. Named-location links              -> LOCATION_BIOME_MAP
    """
    if not html or len(html) < 1000:
        return []

    biomes = set()

    # 1. Pal Recruiter section
    for m in re.finditer(r'Pal Recruiter:\s*([A-Za-z_][A-Za-z0-9_]*)', html):
        bid = m.group(1)
        if bid in PALDB_BIOME_ID_MAP:
            biomes.add(PALDB_BIOME_ID_MAP[bid])
        elif bid in STANDARD_BIOMES:
            biomes.add(bid)

    # 2. zone= param in hrefs
    for m in re.finditer(r'zone=([a-z][a-z0-9]*)_grade_\d+', html):
        zone = m.group(1)
        for prefix, biome in ZONE_PREFIX_MAP.items():
            if zone.startswith(prefix):
                biomes.add(biome)
                break

    # 3. spawner= param in hrefs.
    # Format: spawner=<area>[_<zone>[_<subtype>...]]
    # Examples: 81_1_grass_FBOSS_2, worldtree_9_55_WorldTreeAura,
    #           skyisland_8_04_B_highland_FBOSS_1, yamijima_IceLand_pink_B,
    #           sanctuary_3_dessert, yellow_D, desert_orange_C
    for m in re.finditer(r'spawner=([A-Za-z][A-Za-z0-9]*)', html):
        area = m.group(1)
        if area in SPAWNER_AREA_MAP:
            biomes.add(SPAWNER_AREA_MAP[area])

    # 4. Inside spawner=... value, look for type keywords (grass, snow, etc.)
    for m in re.finditer(r'spawner=[A-Za-z0-9_]*?(grass|forest|desert|dessert|snow|volcano|dark|sky|moon|feybreak|sakurajima|sanctuary|tropical|island|yellow|worldtree|skyisland|yamijima|remainsIsland|Ocean|volcanoiskand|sakura)[A-Za-z0-9_]*', html):
        kw = m.group(1)
        if kw in ZONE_PREFIX_MAP:
            biomes.add(ZONE_PREFIX_MAP[kw])
        elif kw in SPAWNER_AREA_MAP:
            biomes.add(SPAWNER_AREA_MAP[kw])

    # 4. Named locations
    for m in re.finditer(r'href="([A-Za-z0-9_]+)"', html):
        href = m.group(1)
        for key, biome in LOCATION_BIOME_MAP.items():
            if key in href:
                biomes.add(biome)

    return sorted(biomes)


def is_standard_biome_list(biomes):
    """True if every entry is in the standard list."""
    return all(b in STANDARD_BIOMES for b in biomes)


# --- Main --------------------------------------------------------------------
def main():
    pals = json.load(open(PALS_JSON, encoding='utf-8'))
    by_id = {p['id']: p for p in pals}
    total = len(pals)
    initial_with = sum(1 for p in pals if p.get('biomes'))
    print('=== fill-biomes start ===')
    print('Total pals:        %d' % total)
    print('Already have biomes: %d' % initial_with)
    print('Missing biomes:      %d' % (total - initial_with))
    print()

    # Classify the missing ones
    need = [p for p in pals if not p.get('biomes')]
    special = []
    variants = []
    bases = []
    for p in need:
        pid = p['id']
        is_var, base_id = split_base_variant(pid)
        if pid in SPECIAL_BIOMES:
            special.append(p)
        elif is_var:
            variants.append((p, base_id))
        else:
            bases.append(p)
    print('Classified: %d special, %d variant, %d base' % (len(special), len(variants), len(bases)))
    print()

    report = []
    def log(msg):
        print(msg)
        report.append(msg)

    # ---- 1. Hardcoded specials ----------------------------------------------
    log('--- 1. Hardcoded specials ---')
    hardcoded = 0
    for p in special:
        pid = p['id']
        if pid in SPECIAL_BIOMES:
            p['biomes'] = list(SPECIAL_BIOMES[pid])
            p['updatedAt'] = '2026-07-28'
            hardcoded += 1
            log('  HARDCODE %-25s -> %s' % (pid, p['biomes']))
    log('  hardcoded: %d' % hardcoded)
    log('')

    # ---- 2. Bases + variants: try paldb.cc FIRST so variants can copy after -
    fetch_targets = [p for p in pals if not p.get('biomes')]
    log('--- 2. paldb.cc fetch (%d targets) ---' % len(fetch_targets))
    paldb_hits = []
    paldb_misses = []
    if fetch_targets:
        names = [slug_to_paldb_name(p['id']) for p in fetch_targets]
        t0 = time.time()
        html_map = fetch_paldb_parallel(names, max_workers=4)
        elapsed = time.time() - t0
        log('  fetched %d pages in %.1fs' % (len(names), elapsed))
        for p in fetch_targets:
            pid = p['id']
            paldb_name = slug_to_paldb_name(pid)
            html = html_map.get(paldb_name)
            biomes = parse_biomes_from_paldb(html)
            if biomes:
                p['biomes'] = biomes
                p['updatedAt'] = '2026-07-28'
                paldb_hits.append((pid, biomes))
            else:
                paldb_misses.append(pid)
    log('  paldb_hits: %d' % len(paldb_hits))
    log('  paldb_misses: %d' % len(paldb_misses))
    log('')

    # ---- 3. Variants: copy from base (overrides paldb results for variants)
    # Variants share spawn locations with their base pal, so always prefer base
    # biomes (English or Chinese->English translated) over paldb direct fetch.
    log('--- 3. Variants: copy from base (overrides paldb) ---')
    variant_copied = 0
    variant_translated = 0
    variant_paldb_kept = []
    variant_no_standard_base = []
    for v, base_id in variants:
        base = by_id.get(base_id)
        if not base or not base.get('biomes'):
            # base has no biomes; keep whatever paldb gave us (may be empty)
            if v.get('biomes'):
                variant_paldb_kept.append((v, v['biomes']))
            else:
                variant_no_standard_base.append((v, base_id, None))
            continue
        base_biomes = base['biomes']
        if is_standard_biome_list(base_biomes):
            v['biomes'] = list(base_biomes)
            v['updatedAt'] = '2026-07-28'
            variant_copied += 1
        else:
            translated = []
            for b in base_biomes:
                if b in CHINESE_BIOME_MAP:
                    translated.append(CHINESE_BIOME_MAP[b])
                elif b in STANDARD_BIOMES:
                    translated.append(b)
            if translated:
                v['biomes'] = sorted(set(translated))
                v['updatedAt'] = '2026-07-28'
                variant_translated += 1
            else:
                # base has unknown biomes, keep paldb result
                if v.get('biomes'):
                    variant_paldb_kept.append((v, v['biomes']))
                else:
                    variant_no_standard_base.append((v, base_id, base_biomes))
    log('  variant_copied (English):   %d' % variant_copied)
    log('  variant_translated (Chinese->English): %d' % variant_translated)
    log('  variant_paldb_kept (no standard base): %d' % len(variant_paldb_kept))
    log('  variants still empty: %d' % len(variant_no_standard_base))
    for v, bid, bbm in variant_no_standard_base:
        log('    %-25s -> base=%s base_biomes=%s' % (v['id'], bid, bbm))
    log('')

    # ---- 4. Still empty -> leave [] -----------------------------------------
    final_missing = [p for p in pals if not p.get('biomes')]
    log('--- 4. Still empty after all steps ---')
    log('  empty count: %d' % len(final_missing))
    for p in final_missing:
        log('    %s paldeckNo=%d types=%s' % (p['id'], p.get('paldeckNo', 0), p.get('types', [])))
    log('')

    # ---- Final stats --------------------------------------------------------
    final_with = sum(1 for p in pals if p.get('biomes'))
    log('=== Summary ===')
    log('Before: %d pals with biomes' % initial_with)
    log('After:  %d pals with biomes' % final_with)
    log('Filled: %d' % (final_with - initial_with))
    log('By source:')
    log('  hardcoded specials: %d' % hardcoded)
    log('  variant copy from base: %d' % variant_copied)
    log('  variant translated (Chinese->English): %d' % variant_translated)
    log('  variant kept paldb (no standard base): %d' % len(variant_paldb_kept))
    log('  paldb.cc parse hit: %d' % len(paldb_hits))
    log('  still empty: %d' % len(final_missing))

    # ---- Write back ---------------------------------------------------------
    with open(PALS_JSON, 'w', encoding='utf-8') as f:
        json.dump(pals, f, ensure_ascii=False, indent=0)
    log('')
    log('Wrote ' + PALS_JSON)

    # Save report
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))
    log('Wrote ' + REPORT_FILE)


if __name__ == '__main__':
    main()
