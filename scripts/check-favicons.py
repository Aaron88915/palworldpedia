#!/usr/bin/env python3
import urllib.request
for u in ['/favicon.ico', '/favicon.svg', '/favicon-32.png', '/apple-touch-icon.png']:
    try:
        req = urllib.request.Request(f'https://palworldpedia.cc{u}', headers={'User-Agent': 'Mozilla/5.0'})
        r = urllib.request.urlopen(req, timeout=10)
        size = len(r.read())
        ct = r.headers.get('content-type', '')
        print(f'  palworldpedia.cc{u:<30} {r.status}  size={size}  type={ct}')
    except Exception as e:
        print(f'  {u}: {e}')
