#!/usr/bin/env python3
import urllib.request, re

req = urllib.request.Request('https://paldb.cc/en/Lamball', headers={'User-Agent': 'Mozilla/5.0'})
c = urllib.request.urlopen(req, timeout=15).read().decode('utf-8', 'ignore')

# 找地图/biome 区域
# 试找 "habitat" / "biome" / 地图
patterns = [
    r'habitat[\s\S]{0,500}',
    r'biome[\s\S]{0,300}',
    r'map[\s\S]{0,200}',
    r'location[\s\S]{0,200}',
]
for pat in patterns:
    matches = re.findall(pat, c, re.IGNORECASE)
    if matches:
        print(f'=== {pat[:30]}... ===')
        for m in matches[:2]:
            text = re.sub(r'<[^>]+>', ' ', m)
            text = re.sub(r'\s+', ' ', text).strip()
            print(f'  {text[:300]}')
        print()
