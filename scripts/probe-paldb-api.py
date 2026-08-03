#!/usr/bin/env python3
import urllib.request
for url in [
    'https://paldb.cc/api/v1/pal/Lamball',
    'https://paldb.cc/api/pal/Lamball',
    'https://paldb.cc/api/Lamball',
    'https://paldb.cc/api/v1/pals',
    'https://paldb.cc/en/api/Lamball',
    'https://paldb.cc/data/Lamball',
    'https://paldb.cc/en/Pal/Lamball',
    'https://paldb.cc/en/Paldeck',
]:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json'})
        r = urllib.request.urlopen(req, timeout=10)
        body = r.read().decode('utf-8', 'ignore')[:200]
        ct = r.headers.get('content-type')
        print(f'{url}  {r.status}  type={ct}')
        print(f'  body: {body[:150]}')
    except Exception as e:
        print(f'{url}  ERR: {str(e)[:80]}')
