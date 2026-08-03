#!/usr/bin/env python3
import urllib.request
for u in ['https://palworldpedia.cc/sitemap-index.xml', 'https://palworldpedia.cc/sitemap-0.xml']:
    req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
    r = urllib.request.urlopen(req, timeout=15)
    body = r.read().decode('utf-8', 'ignore')
    print(f'=== {u} ===')
    if 'sitemapindex' in body:
        print(body)
    else:
        # 找第一个 url 节点 + 最后一个
        import re
        m = re.search(r'<url>.*?</url>', body, re.DOTALL)
        if m:
            print('First url:')
            print(m.group(0))
        # 最后一个
        matches = list(re.finditer(r'<url>.*?</url>', body, re.DOTALL))
        if len(matches) > 1:
            print(f'\nLast url (of {len(matches)}):')
            print(matches[-1].group(0))
        print(f'\nTotal size: {len(body)} bytes')
        print(f'Total <url> nodes: {len(matches)}')
    print()
