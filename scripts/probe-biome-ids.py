# -*- coding: utf-8 -*-
"""Fetch paldb.cc pages and collect all unique Pal Recruiter biome names."""
import urllib.request, json, re, time

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# Test with several different pals to find all biome names
TEST_PALS = ['Lamball', 'Cattiva', 'Chikipi', 'Lifmunk', 'Mau', 'Celaray', 'Fuack',
             'Pengullet', 'Melpaca', 'Cawgnito', 'Gumoss', 'Mozzarina', 'Faleris',
             'Jormuntide', 'Grizzbolt', 'Orserk', 'Frostallion', 'Jetragon', 'Necromus']

def get_recruiter_biomes(html, pal_name):
    """Extract Pal Recruiter biome names from a pal page."""
    # Find the Pal Recruiter section
    m = re.search(r'Pal Recruiter(.*?)(?=<h[1-6]|<section|<div class="col-12">)', html, re.DOTALL)
    if not m:
        return []
    text = re.sub(r'<[^>]+>', ' ', m.group(1))
    text = re.sub(r'\s+', ' ', text).strip()
    # Parse: "BiomeName 0.06% PalName Lv. X-Y"
    biomes = re.findall(r'([A-Z][a-zA-Z_]+)\s+\d+\.?\d*%', text)
    return list(dict.fromkeys(biomes))  # dedupe preserving order

all_biomes = set()
for pal in TEST_PALS:
    url = f'https://paldb.cc/en/{pal}'
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        r = urllib.request.urlopen(req, timeout=15)
        html = r.read().decode('utf-8', errors='ignore')
        biomes = get_recruiter_biomes(html, pal)
        print(f'{pal:15s}: {biomes}')
        all_biomes.update(biomes)
    except Exception as e:
        print(f'{pal}: ERR {e}')
    time.sleep(0.3)

print(f'\nAll biomes seen ({len(all_biomes)}):')
for b in sorted(all_biomes):
    print(f'  {b}')
