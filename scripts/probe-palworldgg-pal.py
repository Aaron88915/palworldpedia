# -*- coding: utf-8 -*-
"""Probe palworld.gg for the first pal to find URL pattern + image."""
import urllib.request, re

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

# Try Fuack (common pal)
for url in [
    'https://palworld.gg/pals/Fuack',
    'https://palworld.gg/pals/fuack',
    'https://palworld.gg/pals/Lamball',
    'https://palworld.gg/pals/lamball',
    'https://palworld.gg/pals/Cattiva',
    'https://palworld.gg/pals/cattiva',
]:
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        r = urllib.request.urlopen(req, timeout=15)
        d = r.read().decode('utf-8', errors='ignore')
        print(f'\n=== {url} (status={r.status}, len={len(d)}) ===')
        # Find pal image (not logo/icon)
        imgs = re.findall(r'<img[^>]+src="([^"]+)"', d)
        for img in imgs[:10]:
            if 'cloudfront' in img or 'palworld' in img or 'cloudinary' in img or 'pals/' in img or 'pal-' in img or '/pal' in img.lower():
                print(f'  IMG: {img[:250]}')
        # Find data attributes that might have image
        for m in re.finditer(r'(?:src|data-src|srcset)=["\']([^"\']*\.(?:webp|png|jpg|jpeg|avif)[^"\']*)["\']', d):
            print(f'  DATA: {m.group(1)[:250]}')
    except Exception as e:
        print(f'{url}: ERR {e}')
