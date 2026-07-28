# -*- coding: utf-8 -*-
"""Fetch palworld.gg /pals payload.json and extract pal slugs + image URLs."""
import urllib.request, re, json

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

# Get the payload
req = urllib.request.Request('https://palworld.gg/pals/_payload.json', headers=HEADERS)
r = urllib.request.urlopen(req, timeout=20)
d = r.read()
print(f'Payload size: {len(d)}')

# Try to find a data path
# Save the raw payload
with open('scripts/palworldgg-pals-payload.json', 'wb') as f:
    f.write(d)

# The payload is a Nuxt serialized structure. Try to parse.
try:
    j = json.loads(d)
    print(f'Type: {type(j).__name__}, length: {len(j) if hasattr(j, "__len__") else "?"}')
    if isinstance(j, list):
        print(f'First item type: {type(j[0]).__name__}')
        if isinstance(j[0], dict):
            print(f'First item keys: {list(j[0].keys())[:10]}')
        else:
            print(f'First item: {j[0][:200] if isinstance(j[0], str) else j[0]}')
except Exception as e:
    print(f'JSON parse failed: {e}')
