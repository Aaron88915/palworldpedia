#!/usr/bin/env python3
import re
c = open('dist/breeding/index.html', encoding='utf-8').read()
# 找 "完整配种表" 前后位置
m = re.search(r'完整配种表', c)
if m:
    pos = m.start()
    # 打印 byte @pos 前后 600 字符
    start = max(0, pos - 400)
    end = min(len(c), pos + 200)
    snippet = c[start:end]
    # 替换 \n 为 | 看
    snippet = re.sub(r'>\s*<', '>\n<', snippet)
    print(snippet)
