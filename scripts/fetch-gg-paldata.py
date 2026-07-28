# -*- coding: utf-8 -*-
import urllib.request, json
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
url = 'https://palworld.gg/_nuxt/data/pals/en.json'
req = urllib.request.Request(url, headers=HEADERS)
d = urllib.request.urlopen(req, timeout=30).read()
print(f'Size: {len(d)}')
with open('scripts/palworldgg-pals-en.json', 'wb') as f:
    f.write(d)
j = json.loads(d)
print(f'JSON type: {type(j).__name__}, len: {len(j) if hasattr(j, "__len__") else "?"}')
if isinstance(j, list):
    print('First item keys:', list(j[0].keys())[:20] if j else 'empty')
    if j:
        print('Sample:')
        print(json.dumps(j[0], ensure_ascii=False, indent=2)[:500])
elif isinstance(j, dict):
    print('Keys:', list(j.keys())[:10])
