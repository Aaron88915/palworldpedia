#!/usr/bin/env python3
import urllib.request, re
req = urllib.request.Request('https://paldb.cc/en/Map', headers={'User-Agent': 'Mozilla/5.0'})
c = urllib.request.urlopen(req, timeout=15).read().decode('utf-8', 'ignore')
# 找所有 location 链接
links = re.findall(r'href="(/en/[A-Z][a-zA-Z]+)"[^>]*>([^<]{2,50})<', c)
seen = set()
for url, text in links:
    if any(k in url.lower() for k in ['map', 'island', 'mount', 'forest', 'desert', 'volcano', 'shore', 'dune', 'ruin', 'tundra', 'windswept']):
        key = (url, text)
        if key not in seen:
            seen.add(key)
            print(f'  {url}  |  {text.strip()}')

# 找所有可能的 biome 名（Palpagos Islands 上下文）
print('\n=== 找所有 location 区域名 ===')
for kw in ['Palpagos', 'Sakurajima', 'Isle', 'Mountain', 'Plateau', 'Forest', 'Desert', 'Volcano', 'Shore', 'Dunes', 'Tundra', 'Sanctum', 'Cavern']:
    m = re.findall(rf'>([A-Z][^<]{{2,50}}{kw}[^<]{{0,30}})<', c)
    for x in m[:3]:
        if x.strip() and '<' not in x:
            print(f'  {kw}: {x.strip()}')
