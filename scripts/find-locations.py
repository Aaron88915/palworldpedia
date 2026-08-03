#!/usr/bin/env python3
import urllib.request, re
req = urllib.request.Request('https://paldb.cc/en/Lamball', headers={'User-Agent': 'Mozilla/5.0'})
c = urllib.request.urlopen(req, timeout=15).read().decode('utf-8', 'ignore')

# 找所有 "fa-map" 图标附近的 href 链接（可能是 location links）
m = re.findall(r'href="(/en/[^"]+)"[^>]*>[^<]*<[^>]*fa-map', c)
print('Locations via fa-map icon:')
for x in m[:20]:
    print(f'  {x}')

# 找所有 class 含 "text-truncate" 的链接
m = re.findall(r'class="[^"]*text-truncate[^"]*"[^>]*>([^<]{2,50})<', c)
print('\ntext-truncate elements:')
for x in m[:30]:
    print(f'  {x.strip()}')

# 找 Palpagos Islands 周围
m = re.search(r'Palpagos Islands[\s\S]{0,2000}', c)
if m:
    seg = m.group(0)
    print('\nPalpagos Islands 周围:')
    for m2 in re.finditer(r'>([^<]{2,60})<', seg[:1500]):
        t = m2.group(1).strip()
        if t and t not in ['', ' ']:
            print(f'  {t}')

# 找 a 标签里 href 是 location 类的
m = re.findall(r'href="(/en/location[^"]+|/en/map[^"]+)"[^>]*>([^<]{2,50})<', c)
print('\nLocation links:')
for url, text in m[:20]:
    print(f'  {url}  |  {text.strip()}')
