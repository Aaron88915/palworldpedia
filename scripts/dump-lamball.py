# -*- coding: utf-8 -*-
import urllib.request, json, re

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

req = urllib.request.Request('https://paldb.cc/en/Lamball', headers=HEADERS)
r = urllib.request.urlopen(req, timeout=15)
data = r.read().decode('utf-8', errors='ignore')

# Look for script blocks with data
scripts = re.findall(r'<script[^>]*src="([^"]+)"', data)
print('External scripts:')
for s in scripts[:10]:
    print(f'  {s}')

# Find __NEXT_DATA__ or similar SSR data
m = re.search(r'<script[^>]*id="__NEXT_DATA__"[^>]*>(.*?)</script>', data, re.DOTALL)
if m:
    print(f'\n__NEXT_DATA__ found, {len(m.group(1))} chars')
    try:
        j = json.loads(m.group(1))
        # Look for biome data
        def find_biomes(obj, path=''):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if 'biome' in k.lower() or 'location' in k.lower() or 'spawn' in k.lower():
                        print(f'  {path}.{k}: {str(v)[:200]}')
                    find_biomes(v, f'{path}.{k}')
            elif isinstance(obj, list):
                for i, v in enumerate(obj[:50]):
                    find_biomes(v, f'{path}[{i}]')
        find_biomes(j)
    except Exception as e:
        print(f'JSON parse error: {e}')

# Look for any inline JSON with biomes
print('\nLooking for biome keywords:')
for kw in ['Windswept', 'Sea Breeze', 'Marsh Island', 'Isle of Murmurs', 'Sakurajima', 'biome', 'habitat']:
    if kw in data:
        idx = data.find(kw)
        ctx = data[max(0, idx-100):idx+200].replace('\n', ' ')
        print(f'  [{kw}] at {idx}: ...{ctx}...')
