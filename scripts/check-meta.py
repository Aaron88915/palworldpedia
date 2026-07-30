#!/usr/bin/env python3
import urllib.request, re

# 抓现场 EN 首页 meta description
req = urllib.request.Request('https://palworldpedia.cc/en/', headers={'User-Agent': 'Mozilla/5.0'})
c = urllib.request.urlopen(req, timeout=15).read().decode('utf-8', 'ignore')

print('=== EN 首页 meta ===')
for m in re.finditer(r'<meta\s+(name|property)="(description|og:description)"[^>]*>', c):
    s = m.group(0)
    # 提取 content
    cm = re.search(r'content="([^"]+)"', s)
    if cm:
        text = cm.group(1)
        print(f'  length: {len(text)}')
        print(f'  content: {text}')

# 中文版
print('\n=== ZH 首页 meta ===')
req = urllib.request.Request('https://palworldpedia.cc/', headers={'User-Agent': 'Mozilla/5.0'})
c = urllib.request.urlopen(req, timeout=15).read().decode('utf-8', 'ignore')
for m in re.finditer(r'<meta\s+(name|property)="(description|og:description)"[^>]*>', c):
    s = m.group(0)
    cm = re.search(r'content="([^"]+)"', s)
    if cm:
        text = cm.group(1)
        print(f'  length: {len(text)}')
        print(f'  content: {text}')

# 推荐长度：Google 显示 ~155-160 字符；Bing 推荐 < 160
print('\n参考：')
print('  Bing 推荐: < 160 字符')
print('  Google 显示: 155-160 字符')
