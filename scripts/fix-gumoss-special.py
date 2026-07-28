# -*- coding: utf-8 -*-
"""Use base Gumoss image as fallback for Gumoss Special."""
import urllib.request, os, re

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

# Get Gumoss icon name from palworld.gg
with open('scripts/palworldgg-bundles/CK2A4_hG.js', encoding='utf-8') as f:
    d = f.read()
m = re.search(r'slug:"gumoss"[^}]*?icon:"([^"]+)"', d)
if m:
    icon = m.group(1)
    print(f'Gumoss icon: {icon}')
    url = f'https://palworld.gg/images/full_palicon/{icon}.png'
    req = urllib.request.Request(url, headers=HEADERS)
    data = urllib.request.urlopen(req, timeout=20).read()
    save_path = 'public/images/pals/Gumoss (Special).png'
    with open(save_path, 'wb') as f:
        f.write(data)
    print(f'Saved {save_path} ({len(data)} bytes)')
