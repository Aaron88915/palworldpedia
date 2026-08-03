#!/usr/bin/env python3
import urllib.request, re
req = urllib.request.Request('https://paldb.cc/en/Lamball', headers={'User-Agent': 'Mozilla/5.0'})
c = urllib.request.urlopen(req, timeout=15).read().decode('utf-8', 'ignore')

# 找所有以 "Map" / "Island" / "Mountain" 结尾的字符串（可能是 biome 名）
print('=== 找疑似 biome 名 ===')
candidates = re.findall(r'>([^<>]{2,30}(?:Map|Island|Mountain|Plateau|Forest|Desert|Volcano|Shore|Ravine|City|Ruin|Sea|Sakurajima|Astral|Beach|Snow|Sand|Wind|Lake|Crater|Valley|Plains|Tundra|Swamp|Jungle|River|Lake|Steppe|Highland|Hill)[^<>]{0,20})<', c)
for c2 in candidates[:30]:
    print(f'  {c2.strip()}')

# 找 "Day (xxx)" 后面所有 div 内容
print('\n=== 找 Day 标签后的 li/div ===')
m = re.search(r'Day \(\d+\)[\s\S]{0,4000}', c)
if m:
    segment = m.group(0)
    # 找所有 <li> 内容
    items = re.findall(r'<li[^>]*>([\s\S]{2,500}?)</li>', segment)
    print(f'  found {len(items)} <li> elements')
    for it in items[:10]:
        text = re.sub(r'<[^>]+>', ' ', it)
        text = re.sub(r'\s+', ' ', text).strip()
        if text:
            print(f'  > {text[:100]}')

# 找 JavaScript 里的数据 (window.__NUXT__ / __INITIAL_STATE__)
print('\n=== 找 embedded JSON ===')
for pat in [r'window\.__NUXT__[\s\S]{0,200}', r'__INITIAL_STATE__[\s\S]{0,200}', r'__pinia[\s\S]{0,200}']:
    m = re.search(pat, c)
    if m:
        print(f'  {pat[:30]}: {m.group(0)[:200]}')
