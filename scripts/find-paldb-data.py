# -*- coding: utf-8 -*-
import urllib.request, json, re

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

req = urllib.request.Request('https://paldb.cc/en/Lamball', headers=HEADERS)
r = urllib.request.urlopen(req, timeout=15)
data = r.read().decode('utf-8', errors='ignore')

# Find the EN data (script with all pal data)
# Look for window globals with pal data
patterns = [
    (r'window\.__palData\s*=\s*(\{.*?\});', 'palData'),
    (r'window\.__palworld_data\s*=\s*(\{.*?\});', 'palworld_data'),
    (r'var\s+pals\s*=\s*(\[.*?\]);', 'pals array'),
    (r'window\.pals\s*=\s*(\[.*?\]);', 'pals'),
    (r'/api/pal/(\w+)', 'pal API'),
]

for pat, name in patterns:
    m = re.search(pat, data, re.DOTALL)
    if m:
        print(f'Pattern "{name}" found, {len(m.group(1))} chars')
        # Show first 500
        print(m.group(1)[:500])
        print()

# Look for AJAX calls in JS
api_calls = re.findall(r'url:\s*["\']([^"\']+)["\']', data)
for url in api_calls[:5]:
    print(f'AJAX URL: {url}')

# Look for fetch calls
fetches = re.findall(r'fetch\(["\']([^"\']+)["\']', data)
for url in fetches[:5]:
    print(f'Fetch URL: {url}')

# Look for cache references
caches = list(set(re.findall(r'/cache/[^"\']+\.json', data)))
for c in caches[:5]:
    print(f'Cache: {c}')

# Check the hover cache
hover = re.findall(r'data-hover="([^"]+)"', data)
print(f'\nHover cache URLs: {len(hover)}')
for h in hover[:3]:
    print(f'  {h}')
