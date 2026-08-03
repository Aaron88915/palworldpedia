#!/usr/bin/env python3
import urllib.request, json

# GSC API check (unauthenticated, no index quota but can see status)
print('=== 触发 GSC 重新抓取 ===')

# 通过 indexnow 或 ping
urls = [
    'https://palworldpedia.cc/sitemap-index.xml',
    'https://palworldpedia.cc/sitemap-0.xml',
]

# 用 curl/urllib 模拟 GSC 验证
for u in urls:
    try:
        req = urllib.request.Request(u, headers={
            'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'palworldpedia.cc',
        })
        r = urllib.request.urlopen(req, timeout=15)
        body = r.read()
        print(f'  {u}')
        print(f'    status={r.status}  size={len(body)}  ct={r.headers.get("content-type")}')
        print(f'    server={r.headers.get("server", "n/a")}')
    except Exception as e:
        print(f'  {u}: {e}')

# 检查 sitemap 的 Content-Encoding
print()
print('=== 用 HEAD 方法 ===')
import urllib.request
req = urllib.request.Request('https://palworldpedia.cc/sitemap-0.xml', method='HEAD', headers={'User-Agent': 'Googlebot/2.1'})
try:
    r = urllib.request.urlopen(req, timeout=10)
    print(f'  HEAD status: {r.status}')
    for k, v in r.headers.items():
        print(f'    {k}: {v}')
except Exception as e:
    print(f'  {e}')
