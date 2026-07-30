#!/usr/bin/env python3
import re
c = open('dist/breeding/index.html', encoding='utf-8').read()
# 找 breeding 关键字 "完整配种表"（在 source 里 inline 之后）
m = re.search(r'完整配种表', c)
if m:
    # 打印前后 1500 字符
    start = max(0, m.start() - 1500)
    end = min(len(c), m.end() + 200)
    snippet = c[start:end]
    snippet = re.sub(r'\s+', ' ', snippet)
    print(snippet)
else:
    print('NOT FOUND')
