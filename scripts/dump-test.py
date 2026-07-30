#!/usr/bin/env python3
import re
c = open('dist/test-adslot/index.html', encoding='utf-8').read()
# 找 body 内容
m = re.search(r'<body[^>]*>(.*?)</body>', c, re.DOTALL)
if m:
    body = m.group(1)
    body = re.sub(r'>\s*<', '>\n<', body)
    print(body[:3000])
