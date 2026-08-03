#!/usr/bin/env python3
import urllib.request, re

req = urllib.request.Request('https://paldb.cc/en/Lamball', headers={'User-Agent': 'Mozilla/5.0'})
c = urllib.request.urlopen(req, timeout=15).read().decode('utf-8', 'ignore')

# 找 "Day (351)" 附近的内容
m = re.search(r'Day \(\d+\)[\s\S]{0,3000}', c)
if m:
    text = m.group(0)
    # 找 id="xxx" 的所有 div
    print('=== Around Day(N) ===')
    for m2 in re.finditer(r'(?:id|class)="([^"]+)"[^>]*>([^<]{2,80})<', text[:2500]):
        if m2.group(2).strip():
            print(f'  {m2.group(1)[:30]:<32} | {m2.group(2)[:60]}')

# 找 "map-area" / "map_area" 区域
print('\n=== map area ===')
m = re.search(r'id="map-area"[\s\S]{0,5000}', c) or re.search(r'class="map[\s\S]{0,2000}', c)
if m:
    for m2 in re.finditer(r'(?:id|class)="([^"]*map[^"]*)"[^>]*>([^<]{0,80})<', m.group(0)[:3000]):
        print(f'  {m2.group(1)[:40]:<42} | {m2.group(2)[:60]}')
