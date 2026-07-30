#!/usr/bin/env python3
import urllib.request, re
req = urllib.request.Request('https://palworldpedia.cc/', headers={'User-Agent': 'Mozilla/5.0'})
c = urllib.request.urlopen(req, timeout=15).read().decode('utf-8', 'ignore')
# 找 header 区域
m = re.search(r'<header[^>]*>(.*?)</header>', c, re.DOTALL)
if m:
    # 在 header 里找 EN
    h = m.group(1)
    # 找所有包含 'EN' 的 a 标签
    for m2 in re.finditer(r'<a[^>]*>[^<]*EN[^<]*</a>', h):
        print(m2.group(0))
    print('--- header snippet (last 1500 chars) ---')
    print(h[-1500:])
