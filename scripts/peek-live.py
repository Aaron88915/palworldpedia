# -*- coding: utf-8 -*-
import urllib.request

for slug in ['gumoss-special', 'cryolinx-terra']:
    url = f'https://palworldpedia.cc/pals/{slug}/'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'})
    r = urllib.request.urlopen(req, timeout=15)
    html = r.read().decode('utf-8')
    print(f'=== {slug} (len={len(html)}) ===')
    # Print just the body main content
    start = html.find('<body')
    body = html[start:] if start > 0 else html
    # Strip newlines/extra spaces for compactness
    body = body.replace('\n', ' ').replace('  ', ' ')[:6000]
    print(body)
    print()
