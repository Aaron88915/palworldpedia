#!/usr/bin/env python3
import urllib.request, re

req = urllib.request.Request('https://paldb.cc/en/Lamball', headers={'User-Agent': 'Mozilla/5.0'})
c = urllib.request.urlopen(req, timeout=15).read().decode('utf-8', 'ignore')

# 找所有 class 含 "biome" / "habitat" / "map" 的
for tag, label in [
    (r'class="[^"]*biome[^"]*"', 'biome'),
    (r'class="[^"]*habitat[^"]*"', 'habitat'),
    (r'class="[^"]*location[^"]*"', 'location'),
    (r'class="[^"]*map_name[^"]*"', 'map_name'),
    (r'class="[^"]*area_name[^"]*"', 'area_name'),
]:
    matches = re.findall(tag, c, re.IGNORECASE)
    if matches:
        print(f'=== {label} ({len(matches)} 个) ===')
        seen = set()
        for m in matches[:20]:
            if m in seen:
                continue
            seen.add(m)
            print(f'  {m[:200]}')
        print()

# 找 "Day (xxx)" / "Night (xxx)" 里的数字 (总数)
m = re.findall(r'Day \((\d+)\)', c)
n = re.findall(r'Night \((\d+)\)', c)
if m or n:
    print(f'Day count: {m[0] if m else "?"}  Night count: {n[0] if n else "?"}')

# 找 "Tower Raid" / "Tutorial Island" 等已知地点
known_locations = [
    'Tutorial Island', 'Hillside Plateau', 'Forest', 'Desert', 'Volcano',
    'Astral Mountain', 'Moonless Shore', 'Iceberg', 'Sea', 'Sakurajima',
    'Mount Obsidian', 'Dawn Ravine', 'Ruined City', 'Fort Ruin',
    'Sanctum of the Annihilator',
]
for loc in known_locations:
    if loc in c:
        print(f'  found: {loc}')
