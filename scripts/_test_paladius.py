# -*- coding: utf-8 -*-
"""Test the parser on boss pals."""
import re, os

PALDB_BIOME_ID_MAP = {
    'Forest_Volcano': 'Mount Obsidian',
    'DarkIsland':     'Isle of Silence',
    'Desert_Snow':    'Astral Mountains',
    'Grass':          'Marsh Island',
    'Sakurajima':     'Sakurajima',
    'SkyIsland':      'Sea Breeze Archipelago',
    'MoonIsle':       'Isle of Murmurs',
}
ZONE_PREFIX_MAP = {
    'grass':      'Marsh Island',
    'forest':     'Windswept Island',
    'desert':     'Twilight Dunes',
    'dessert':    'Twilight Dunes',
    'snow':       'Astral Mountains',
    'volcano':    'Mount Obsidian',
    'dark':       'Isle of Silence',
    'sky':        'Sea Breeze Archipelago',
    'moon':       'Isle of Murmurs',
    'feybreak':   'Feybreak',
    'sakurajima': 'Sakurajima',
    'sanctuary':  'Wildlife Sanctuary',
}
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
STANDARD_BIOMES = {
    'Windswept Island', 'Sea Breeze Archipelago', 'Marsh Island', 'Eastern Wild Island',
    'Isle of Murmurs', 'Isle of Silence', 'Bamboo Groves', 'Twilight Dunes',
    'Astral Mountains', 'Mount Obsidian', 'Sakurajima', 'Feybreak',
    'Wildlife Sanctuary', 'No. 1 Wildlife Sanctuary', 'No. 2 Wildlife Sanctuary', 'No. 3 Wildlife Sanctuary',
    'Sealed Realms', 'Dungeons', 'Alpha Pals', 'Enemies', 'Rampaging', 'Tower',
    'Palpagos Islands',
}

def parse_biomes(html):
    if not html or len(html) < 1000:
        return []
    biomes = set()
    for m in re.finditer(r'Pal Recruiter:\s*([A-Za-z_][A-Za-z0-9_]*)', html):
        bid = m.group(1)
        if bid in PALDB_BIOME_ID_MAP:
            biomes.add(PALDB_BIOME_ID_MAP[bid])
        elif bid in STANDARD_BIOMES:
            biomes.add(bid)
    for m in re.finditer(r'zone=([a-z][a-z0-9]*)_grade_\d+', html):
        zone = m.group(1)
        for prefix, biome in ZONE_PREFIX_MAP.items():
            if zone.startswith(prefix):
                biomes.add(biome)
                break
    for m in re.finditer(r'spawner=[A-Za-z0-9_]*?(grass|forest|desert|dessert|snow|volcano|dark|sky|moon|feybreak|sakurajima|sanctuary)[A-Za-z0-9_]*', html):
        prefix = m.group(1)
        if prefix in ZONE_PREFIX_MAP:
            biomes.add(ZONE_PREFIX_MAP[prefix])
    for m in re.finditer(r'href="([A-Za-z0-9_]+)"', html):
        href = m.group(1)
        for key, biome in LOCATION_BIOME_MAP.items():
            if key in href:
                biomes.add(biome)
    return sorted(biomes)


cache_dir = 'scripts/_paldb_cache'
for name in ['Paladius', 'Necromus', 'Frostallion', 'Bellanoir', 'Bellanoir_Libero', 'Jormuntide', 'Jormuntide_Ignis', 'Faleris', 'Faleris_Aqua', 'Suzaku_Aqua', 'Suzaku', 'Grizzbolt', 'Orserk']:
    path = os.path.join(cache_dir, name + '.html')
    if not os.path.exists(path):
        print('%-25s NO CACHE' % name)
        continue
    html = open(path, encoding='utf-8', errors='ignore').read()
    biomes = parse_biomes(html)
    print('%-25s -> %s' % (name, biomes))
