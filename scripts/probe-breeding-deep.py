# -*- coding: utf-8 -*-
"""Deep probe palworld.gg breeding-calculator - extract UI structure."""
import urllib.request, re, json

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

url = 'https://palworld.gg/breeding-calculator'
req = urllib.request.Request(url, headers=HEADERS)
r = urllib.request.urlopen(req, timeout=20)
data = r.read().decode('utf-8', errors='ignore')
print(f'len={len(data)}')

# Strip HTML
text = re.sub(r'<script[^>]*>.*?</script>', '', data, flags=re.DOTALL)
text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
text = re.sub(r'<[^>]+>', ' ', text)
text = re.sub(r'\s+', ' ', text).strip()

# Find sections of interest
markers = ['Breeding Combinations', 'Path Finder', 'Breeding Rank', 'Combination', 'Special Combination', 'Dark', 'Legendary']
for m in markers:
    idx = text.find(m)
    if idx > 0:
        print(f'\n--- {m} @ {idx} ---')
        print(text[max(0,idx-100):idx+500])

# Also find the JSON __NEXT_DATA__ payload
nd = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.+?)</script>', data)
if nd:
    j = json.loads(nd.group(1))
    props = j.get('props', {}).get('pageProps', {})
    print(f'\n--- __NEXT_DATA__ keys: {list(props.keys())} ---')
    for k, v in props.items():
        if isinstance(v, str):
            print(f'  {k} (str, {len(v)}): {v[:200]}')
        elif isinstance(v, list):
            print(f'  {k} (list, {len(v)}): {str(v[:3])[:300]}')
        elif isinstance(v, dict):
            print(f'  {k} (dict, {len(v)}): {list(v.keys())[:10]}')
        else:
            print(f'  {k} ({type(v).__name__}): {v}')
