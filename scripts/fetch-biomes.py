# -*- coding: utf-8 -*-
"""Fetch biomes from paldb.cc Pal Recruiter + Wild sections for all 288 pals."""
import urllib.request, json, re, time, sys

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# paldb.cc 内部 biome ID → 中文友好名
BIOME_NAMES = {
    'DarkIsland': '暗月岛',
    'Desert_Snow': '雪原',
    'Forest_Volcano': '火山林',
    'Grass': '草原',
    'Sakurajima': '樱岛',
    'SkyIsland': '云海岛',
    'MoonIsle': '月岛',
}

# Wild 段特定位置（粗略）
WILD_LOCATION_MAP = {
    'Hillside Cavern': '山坡洞穴',
    'Isolated Island Cavern': '孤岛洞穴',
    'Mountaintop Cave': '山顶洞穴',
    'Snowy Mountain Cave': '雪山洞穴',
    'Dessert Mountain Cave': '沙漠洞穴',
}

def fetch(pal_slug, retries=2):
    """Fetch paldb.cc page and return HTML or None."""
    for attempt in range(retries + 1):
        try:
            url = f'https://paldb.cc/en/{pal_slug}'
            req = urllib.request.Request(url, headers=HEADERS)
            r = urllib.request.urlopen(req, timeout=15)
            return r.read().decode('utf-8', errors='ignore')
        except Exception as e:
            if attempt < retries:
                time.sleep(1)
                continue
            return None
    return None

def parse_biomes(html, pal_name):
    """Extract biome names from paldb.cc page."""
    biomes = set()
    detailed = set()

    if not html:
        return [], []

    # 1. Pal Recruiter section: "BiomeName 0.06% PalName Lv. X-Y"
    m = re.search(r'Pal Recruiter(.*?)(?=<h[1-6]|<section|<div class="col-12">)', html, re.DOTALL)
    if m:
        text = re.sub(r'<[^>]+>', ' ', m.group(1))
        # Match: "BiomeName 0.06% PalName Lv."
        for bm in re.findall(r'([A-Z][a-zA-Z_]+)\s+\d+\.?\d*%', text):
            if bm in BIOME_NAMES:
                biomes.add(BIOME_NAMES[bm])

    # 2. Wild section: "(Wild) PalName Lv. X-Y Location1 Location2 ..."
    m = re.search(r'\(Wild\)[^"]*?(?=Pal Recruiter|Boss|Pal Egg|Common Egg|Schema)', html, re.DOTALL)
    if m:
        text = re.sub(r'<[^>]+>', ' ', m.group(1))
        # Find specific location names
        for loc in WILD_LOCATION_MAP:
            if loc in text:
                detailed.add(WILD_LOCATION_MAP[loc])
        # Also find old biome codes like green_A, blue_B
        for code in re.findall(r'\b([a-z]+_[A-Z])\b', text):
            pass  # skip old codes

    return sorted(biomes), sorted(detailed)

def main():
    pals = json.load(open('src/data/pals.json', encoding='utf-8'))
    # Slug map: Fandom title
    slug_to_fandom = json.load(open('scripts/slug-to-fandom-final.json', encoding='utf-8'))
    # Reverse: Fandom title -> slug
    title_to_slug = {v: k for k, v in slug_to_fandom.items()}

    updated = 0
    skipped = 0
    failed = []
    for i, pal in enumerate(pals):
        slug = pal['id']
        if pal.get('biomes') and len(pal['biomes']) > 0:
            skipped += 1
            continue
        # Fandom title case
        title = slug_to_fandom.get(slug)
        if not title:
            skipped += 1
            continue
        # paldb.cc uses Fandom title directly
        paldb_slug = title  # e.g. "Gumoss", "Mau Cryst"
        html = fetch(paldb_slug)
        biomes, detailed = parse_biomes(html, paldb_slug)
        if biomes or detailed:
            # Prefer recruiter biomes, append wild details
            combined = biomes + detailed
            pal['biomes'] = combined
            pal['updatedAt'] = '2026-07-28'
            updated += 1
        if (i + 1) % 30 == 0:
            print(f'  [{i+1}/{len(pals)}] updated={updated} skipped={skipped} failed={len(failed)}', flush=True)
        time.sleep(0.4)  # rate limit

    print(f'\nDone: updated={updated} skipped={skipped} failed={len(failed)}')
    if failed:
        print('Failed slugs:', failed[:10])

    json.dump(pals, open('src/data/pals.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('Saved')

    # Stats
    with_biomes = sum(1 for p in pals if p.get('biomes'))
    print(f'Pals with biomes: {with_biomes}/{len(pals)}')

if __name__ == '__main__':
    main()
