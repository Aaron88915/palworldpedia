# -*- coding: utf-8 -*-
"""Extract __NEXT_DATA__ JSON from palworld.gg breeding-calculator."""
import urllib.request, re, json

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

url = 'https://palworld.gg/breeding-calculator'
req = urllib.request.Request(url, headers=HEADERS)
r = urllib.request.urlopen(req, timeout=20)
data = r.read().decode('utf-8', errors='ignore')

# Find __NEXT_DATA__ payload
nd = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.+?)</script>', data)
if not nd:
    print('NO __NEXT_DATA__ found')
    # Try alternate location
    nd = re.search(r'__NEXT_DATA__\s*=\s*({.+?})\s*;\s*</script>', data, re.DOTALL)
    if not nd:
        print('NO alternate either')
        raise SystemExit(1)

j = json.loads(nd.group(1))
print('Top keys:', list(j.keys()))

# Walk the structure
def walk(obj, depth=0, path='root'):
    if depth > 4:
        return
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, (str, int, float, bool, type(None))):
                if isinstance(v, str) and len(v) > 200:
                    print('  ' * depth + f'{path}.{k} = str({len(v)}): {v[:200]}...')
                else:
                    print('  ' * depth + f'{path}.{k} = {v}')
            elif isinstance(v, list):
                print('  ' * depth + f'{path}.{k} = list({len(v)})')
                if len(v) > 0 and depth < 3:
                    walk(v[0], depth + 1, f'{path}.{k}[0]')
            elif isinstance(v, dict):
                print('  ' * depth + f'{path}.{k} = dict({len(v)} keys: {list(v.keys())[:10]})')
                if depth < 3:
                    walk(v, depth + 1, f'{path}.{k}')
    elif isinstance(obj, list):
        if len(obj) > 0:
            walk(obj[0], depth, f'{path}[0]')

walk(j)
