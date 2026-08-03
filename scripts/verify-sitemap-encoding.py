#!/usr/bin/env python3
import urllib.request, gzip, io

url = 'https://palworldpedia.cc/sitemap-0.xml'

# 不接受 gzip
print('=== 不接受 gzip ===')
req = urllib.request.Request(url, headers={'User-Agent': 'Googlebot/2.1', 'Accept-Encoding': 'identity'})
r = urllib.request.urlopen(req, timeout=15)
body = r.read()
print(f'  size={len(body)}  ce={r.headers.get("Content-Encoding")}  ct={r.headers.get("Content-Type")}')

# 接受 gzip
print('\n=== 接受 gzip ===')
req = urllib.request.Request(url, headers={'User-Agent': 'Googlebot/2.1', 'Accept-Encoding': 'gzip'})
r = urllib.request.urlopen(req, timeout=15)
body = r.read()
print(f'  size={len(body)}  ce={r.headers.get("Content-Encoding")}  ct={r.headers.get("Content-Type")}')
if r.headers.get('Content-Encoding') == 'gzip':
    decompressed = gzip.decompress(body)
    print(f'  decompressed size={len(decompressed)}')

# 默认（urllib 可能自动处理）
print('\n=== 默认（urllib auto-decompress）===')
req = urllib.request.Request(url, headers={'User-Agent': 'Googlebot/2.1'})
r = urllib.request.urlopen(req, timeout=15)
body = r.read()
print(f'  size={len(body)}  ce={r.headers.get("Content-Encoding")}  ct={r.headers.get("Content-Type")}')
