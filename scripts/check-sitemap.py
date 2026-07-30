#!/usr/bin/env python3
import urllib.request, re
req = urllib.request.Request('https://palworldpedia.cc/sitemap-0.xml', headers={'User-Agent': 'Mozilla/5.0'})
c = urllib.request.urlopen(req, timeout=15).read().decode('utf-8', 'ignore')

# 第一个 url 节点
m = re.search(r'<url>(.*?)</url>', c, re.DOTALL)
if m:
    print('=== 第一个 url 节点 (前 1500 字符) ===')
    print(m.group(0)[:1500])

# 找带 /en/ 前缀的 url 数量
en_count = len(re.findall(r'<loc>https://palworldpedia\.cc/en/', c))
zh_count = len(re.findall(r'<loc>https://palworldpedia\.cc/(?!en/)', c))
hreflang_count = len(re.findall(r'xhtml:link', c))
print('\n=== URL 分布 ===')
print(f'  zh URL: {zh_count}')
print(f'  en URL: {en_count}')
print(f'  hreflang tag 总数: {hreflang_count}')
print(f'  sitemap 总字节: {len(c)}')
