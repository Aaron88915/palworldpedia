#!/usr/bin/env python3
"""看每个 ins 标签的位置"""
import urllib.request
import re

urls = [
    'https://palworldpedia.cc/',
    'https://palworldpedia.cc/pals/',
    'https://palworldpedia.cc/breeding/',
    'https://palworldpedia.cc/tech-tree/',
    'https://palworldpedia.cc/about/',
]
for u in urls:
    print(f'\n=== {u} ===')
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
        r = urllib.request.urlopen(req, timeout=15)
        c = r.read().decode('utf-8', 'ignore')
        for i, m in enumerate(re.finditer(r'<ins class="adsbygoogle"[^>]*>', c)):
            # 找前后最近的位置标签
            before = c[max(0, m.start()-300):m.start()]
            after = c[m.end():m.end()+150]
            # 找最近的上层 class
            above = re.findall(r'class="[^"]*(ad-slot|ad-placeholder)[^"]*"', before)
            ad_slot = re.findall(r'ad-slot-(top|bottom|inline|sidebar)', before)
            print(f'  #{i+1} @ byte {m.start()}: ad-slot-class={ad_slot}')
    except Exception as e:
        print(f'  ERROR: {e}')
