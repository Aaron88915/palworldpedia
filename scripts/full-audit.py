#!/usr/bin/env python3
import urllib.request, re

print('=== Palworldpedia 全面审计（精简版）===\n')

# 1. OG image
print('1. OG / Twitter image')
for u in ['/og-image.png', '/og-image.jpg', '/og.png']:
    try:
        req = urllib.request.Request(f'https://palworldpedia.cc{u}', headers={'User-Agent': 'Mozilla/5.0'})
        r = urllib.request.urlopen(req, timeout=10)
        size = len(r.read())
        print(f'   {u} → {r.status} {size}B ({r.headers.get("content-type")})')
    except Exception as e:
        print(f'   {u} → {e}')

# 2. og:image meta
print('\n2. 首页 og:image meta')
req = urllib.request.Request('https://palworldpedia.cc/', headers={'User-Agent': 'Mozilla/5.0'})
c = urllib.request.urlopen(req, timeout=10).read().decode('utf-8', 'ignore')
m = re.search(r'<meta\s+property="og:image"\s+content="([^"]+)"', c)
print(f'   {m.group(1) if m else "NOT FOUND"}')

# 3. PWA manifest
print('\n3. PWA manifest')
try:
    req = urllib.request.Request('https://palworldpedia.cc/manifest.json', headers={'User-Agent': 'Mozilla/5.0'})
    r = urllib.request.urlopen(req, timeout=10)
    body = r.read().decode('utf-8', 'ignore')
    print(f'   /manifest.json → {r.status} {len(body)}B')
    print(f'   {body[:200]}')
except Exception as e:
    print(f'   /manifest.json → NOT FOUND')

# 4. 5. 6. 7 抽样首页
print('\n4. 首页 schema 类型')
for m in re.finditer(r'"@type":\s*"([^"]+)"', c):
    print(f'   {m.group(1)}')

print('\n5. 首页 H1 数量')
print(f'   {len(re.findall(r"<h1\b", c))} H1')

print('\n6. 首页图片懒加载')
imgs = re.findall(r'<img[^>]+>', c)
lazy = [i for i in imgs if 'loading="lazy"' in i]
print(f'   {len(lazy)}/{len(imgs)} 懒加载')

print('\n7. 首页缺 alt')
missing = [i for i in imgs if 'alt=' not in i]
print(f'   {len(missing)}/{len(imgs)} 缺 alt')

print('\n8. 首页内/外链')
internal = len(re.findall(r'href="(/[^"]+)"', c))
external = len(re.findall(r'href="(https?://(?!palworldpedia\.cc)[^"]+)"', c))
print(f'   internal: {internal}  external: {external}')

print('\n9. viewport')
m = re.search(r'<meta\s+name="viewport"\s+content="([^"]+)"', c)
print(f'   {m.group(1) if m else "NOT SET"}')

print('\n10. 分析工具')
for pat, label in [
    (r'googletagmanager\.com', 'Google Tag Manager'),
    (r'google-analytics\.com', 'Google Analytics'),
    (r'plausible\.io', 'Plausible'),
]:
    if re.search(pat, c):
        print(f'   {label}: 已配置')
    else:
        print(f'   {label}: 未配置')

# 11. 抽样 1 个帕鲁页 + 1 个 tech 页
print('\n11. 抽样 帕鲁/tech 详情页')

for path, label in [
    ('dist/pals/lamball/index.html', 'pal/lamball'),
    ('dist/tech-tree/Workbench/index.html', 'tech/Workbench'),
    ('dist/breeding/index.html', 'breeding'),
]:
    try:
        content = open(path, encoding='utf-8').read()
        h1 = len(re.findall(r'<h1\b', content))
        imgs = re.findall(r'<img[^>]+>', content)
        lazy = sum(1 for i in imgs if 'loading="lazy"' in i)
        missing_alt = sum(1 for i in imgs if 'alt=' not in i)
        schemas = re.findall(r'"@type":\s*"([^"]+)"', content)
        print(f'   {label}:')
        print(f'     H1={h1}  imgs={len(imgs)} (lazy={lazy}, missing-alt={missing_alt})  schemas={set(schemas)}')
    except Exception as e:
        print(f'   {label}: ERROR {e}')
