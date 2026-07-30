#!/usr/bin/env python3
import urllib.request, re

print('=== 中文版页面 + lang-switch 按钮文字 ===')
for u in ['/', '/pals/', '/breeding/', '/about/']:
    try:
        req = urllib.request.Request(f'https://palworldpedia.cc{u}', headers={'User-Agent': 'Mozilla/5.0'})
        c = urllib.request.urlopen(req, timeout=15).read().decode('utf-8', 'ignore')
        title_m = re.search(r'<title>([^<]+)</title>', c)
        # 找 lang-switch 区域
        switch_m = re.search(r'lang-switch[^>]*>(.*?)</a>', c, re.DOTALL)
        switch_text = re.sub(r'<[^>]+>', '', switch_m.group(1)).strip() if switch_m else 'NO'
        # 找切换到的目标 URL
        href_m = re.search(r'class="lang-switch"[^>]*href="([^"]+)"', c)
        href_m2 = re.search(r'href="([^"]+)"[^>]*class="lang-switch"', c)
        target = (href_m or href_m2)
        target_url = target.group(1) if target else 'NO'
        print(f'  {u:<20} switch-text="{switch_text}"  target={target_url}')
    except Exception as e:
        print(f'  {u}: {e}')

print('\n=== 自动检测脚本（在 head 里）===')
req = urllib.request.Request('https://palworldpedia.cc/', headers={'User-Agent': 'Mozilla/5.0'})
c = urllib.request.urlopen(req, timeout=15).read().decode('utf-8', 'ignore')
m = re.search(r'<script>.*?navigator\.language.*?</script>', c, re.DOTALL)
if m:
    print('Found auto-detect script:')
    print(m.group(0)[:600])
else:
    print('NOT FOUND')
