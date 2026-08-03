#!/usr/bin/env python3
import urllib.request, re
req = urllib.request.Request('https://paldb.cc/en/Lamball', headers={'User-Agent': 'Mozilla/5.0'})
c = urllib.request.urlopen(req, timeout=15).read().decode('utf-8', 'ignore')

# 找所有 script src
scripts = re.findall(r'<script[^>]+src="([^"]+)"', c)
print('External scripts:')
for s in scripts[:20]:
    print(f'  {s}')

# 找 nuxt
m = re.search(r'window\.__NUXT__[\s\S]{0,500}', c)
if m: print(f'\nNUXT: {m.group(0)[:300]}')

# 找 data
m = re.search(r'id="__NEXT_DATA__"[\s\S]{0,500}', c)
if m: print(f'\nNEXT: {m.group(0)[:300]}')
