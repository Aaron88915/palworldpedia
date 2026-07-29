# -*- coding: utf-8 -*-
"""Check what sections exist in a few sample wiki pages."""
import urllib.request, json, urllib.parse, re

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36', 'Accept': 'application/json'}

for title in ['Melpaca', 'Turtacle', 'Cattiva', 'Lamball', 'Lifmunk', 'Pengullet', 'Celaray']:
    url = f'https://palworld.fandom.com/api.php?action=query&format=json&prop=revisions&titles={urllib.parse.quote(title)}&rvprop=content&rvslots=main'
    j = json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=15).read().decode('utf-8'))
    content = list(j['query']['pages'].values())[0]['revisions'][0]['slots']['main']['*']
    print(f'=== {title} (len={len(content)}) ===')
    sections = re.findall(r'^=+\s*([^=]+?)\s*=+\s*$', content, re.MULTILINE)
    for s in sections:
        print(f'  {s}')
    # Check for biomes-like terms
    has_wild = 'Wild Spawn' in content or '== Habitat ==' in content or '== Locations ==' in content
    print(f'  Has Wild Spawn/Habitat/Locations: {has_wild}')
    print()
