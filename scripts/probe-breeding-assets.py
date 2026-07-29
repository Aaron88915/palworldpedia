# -*- coding: utf-8 -*-
"""Find data sources used by palworld.gg/breeding-calculator."""
import urllib.request, re, json

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

url = 'https://palworld.gg/breeding-calculator'
req = urllib.request.Request(url, headers=HEADERS)
r = urllib.request.urlopen(req, timeout=20)
data = r.read().decode('utf-8', errors='ignore')

# Find all script src and link href
scripts = re.findall(r'<script[^>]+src="([^"]+)"', data)
links = re.findall(r'<link[^>]+href="([^"]+)"', data)
print('Scripts:')
for s in scripts[:30]:
    print(f'  {s}')
print('\nStylesheets / data:')
for l in links[:30]:
    print(f'  {l}')

# Look for any API endpoints
print('\n--- API endpoints (string search) ---')
for kw in ['api/', 'json', '/data/', 'fetch(', 'axios', 'breed.json', 'palworld.json']:
    for m in re.finditer(re.escape(kw), data, re.IGNORECASE):
        idx = m.start()
        ctx = data[max(0,idx-50):idx+150]
        # Strip HTML
        ctx = re.sub(r'<[^>]+>', '', ctx)
        print(f'  [{kw}] ...{ctx[:200]}...')
        break

# Look for inline data in <script> blocks
inline = re.findall(r'<script[^>]*>(.*?)</script>', data, re.DOTALL)
print(f'\n--- Inline <script> blocks: {len(inline)} ---')
for i, s in enumerate(inline):
    if len(s) > 200 and ('pals' in s.lower() or 'breed' in s.lower() or 'combi' in s.lower()):
        print(f'\n  Script {i} (len={len(s)}): {s[:500]}')
