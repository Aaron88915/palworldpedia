#!/usr/bin/env python3
import urllib.request, re

# 中文首页
print('=== ZH 首页 (/ ) ===')
req = urllib.request.Request('https://palworldpedia.cc/', headers={'User-Agent': 'Mozilla/5.0'})
c = urllib.request.urlopen(req, timeout=15).read().decode('utf-8', 'ignore')
for tag in ['canonical', 'hreflang', 'description']:
    print(f'\n  {tag}:')
    for m in re.finditer(rf'<link[^>]*{tag}[^>]*>|<meta[^>]*name="{tag}"[^>]*>|<meta[^>]*property="{tag}"[^>]*>', c):
        s = m.group(0)
        print(f'    {s}')

print('\n=== EN 首页 (/en/) ===')
req = urllib.request.Request('https://palworldpedia.cc/en/', headers={'User-Agent': 'Mozilla/5.0'})
c = urllib.request.urlopen(req, timeout=15).read().decode('utf-8', 'ignore')
for tag in ['canonical', 'hreflang', 'description']:
    print(f'\n  {tag}:')
    for m in re.finditer(rf'<link[^>]*{tag}[^>]*>|<meta[^>]*name="{tag}"[^>]*>|<meta[^>]*property="{tag}"[^>]*>', c):
        s = m.group(0)
        print(f'    {s}')
