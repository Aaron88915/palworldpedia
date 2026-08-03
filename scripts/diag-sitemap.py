#!/usr/bin/env python3
import urllib.request, urllib.error

# 用 Googlebot UA 试
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    'Accept': 'application/xml,text/xml,*/*',
}

print('=== 用 Googlebot UA 测试 ===')
for u in [
    'https://palworldpedia.cc/sitemap-index.xml',
    'https://palworldpedia.cc/sitemap-0.xml',
    'https://palworldpedia.cc/',
    'https://palworldpedia.cc/pals/',
]:
    try:
        req = urllib.request.Request(u, headers=HEADERS)
        r = urllib.request.urlopen(req, timeout=15)
        body = r.read()
        ct = r.headers.get('content-type', '')
        print(f'  {u}')
        print(f'    status: {r.status}  size: {len(body)}  type: {ct}')
        # 检查 XML 头
        head = body[:200].decode('utf-8', 'ignore').strip()
        print(f'    head: {head[:80]}')
    except urllib.error.HTTPError as e:
        print(f'  {u}')
        print(f'    ERROR: {e.code} {e.reason}')
    except Exception as e:
        print(f'  {u}')
        print(f'    ERROR: {e}')
