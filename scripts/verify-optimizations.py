#!/usr/bin/env python3
import urllib.request, re

print('=== 验证 4 项优化 ===\n')

# 1. og-image
print('1. og-image.png')
try:
    req = urllib.request.Request('https://palworldpedia.cc/og-image.png', headers={'User-Agent': 'Mozilla/5.0'})
    r = urllib.request.urlopen(req, timeout=10)
    body = r.read()
    print(f'   /og-image.png → {r.status}  {len(body)}B  {r.headers.get("content-type")}')
    # 检查尺寸
    from PIL import Image
    import io
    img = Image.open(io.BytesIO(body))
    print(f'   尺寸: {img.size}')
except Exception as e:
    print(f'   ERROR: {e}')

# 2. Plausible
print('\n2. Plausible')
req = urllib.request.Request('https://palworldpedia.cc/', headers={'User-Agent': 'Mozilla/5.0'})
c = urllib.request.urlopen(req, timeout=10).read().decode('utf-8', 'ignore')
if 'plausible.io' in c:
    m = re.search(r'<script[^>]*plausible[^>]*>', c)
    print(f'   {m.group(0) if m else "found"}')
else:
    print('   NOT FOUND')

# 3. PWA manifest
print('\n3. PWA manifest')
try:
    req = urllib.request.Request('https://palworldpedia.cc/manifest.json', headers={'User-Agent': 'Mozilla/5.0'})
    r = urllib.request.urlopen(req, timeout=10)
    body = r.read().decode('utf-8', 'ignore')
    print(f'   /manifest.json → {r.status}  {len(body)}B')
    import json
    m = json.loads(body)
    print(f'   name: {m.get("name", "?")}')
    print(f'   icons: {len(m.get("icons", []))}')
except Exception as e:
    print(f'   ERROR: {e}')

# 4. Tech schema
print('\n4. Tech page schema')
try:
    req = urllib.request.Request('https://palworldpedia.cc/tech-tree/Workbench/', headers={'User-Agent': 'Mozilla/5.0'})
    c = urllib.request.urlopen(req, timeout=10).read().decode('utf-8', 'ignore')
    schemas = re.findall(r'"@type":\s*"([^"]+)"', c)
    print(f'   schemas: {set(schemas)}')
except Exception as e:
    print(f'   ERROR: {e}')

# 5. Favicon-192 / 512
print('\n5. PWA 图标')
for f in ['favicon-192.png', 'favicon-512.png', 'apple-touch-icon.png']:
    try:
        req = urllib.request.Request(f'https://palworldpedia.cc/{f}', headers={'User-Agent': 'Mozilla/5.0'})
        r = urllib.request.urlopen(req, timeout=10)
        print(f'   /{f} → {r.status}  {len(r.read())}B')
    except Exception as e:
        print(f'   /{f} → ERROR')
