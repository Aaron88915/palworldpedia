#!/usr/bin/env python3
import urllib.request, re

# 找切换器按钮的完整 HTML
for u in ['/', '/en/']:
    try:
        req = urllib.request.Request(f'https://palworldpedia.cc{u}', headers={'User-Agent': 'Mozilla/5.0'})
        c = urllib.request.urlopen(req, timeout=15).read().decode('utf-8', 'ignore')
        m = re.search(r'<a[^>]*class="lang-switch"[^>]*>.*?</a>', c, re.DOTALL)
        if m:
            print(f'  {u}: {m.group(0)}')
        else:
            print(f'  {u}: NO lang-switch anchor found')
    except Exception as e:
        print(f'  {u}: {e}')
