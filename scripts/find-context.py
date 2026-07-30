#!/usr/bin/env python3
import re

# Find the section between power ranking and 9 types in dist/index.html
c = open('dist/index.html', encoding='utf-8').read()

# 找 power ranking 区域结束的 </section>
# 9 大属性开头 "9 大属性"
print('=== 找 "9 大属性" ===')
m = re.search(r'9 大属性', c)
if m:
    # 打印前后 600 字符
    start = max(0, m.start() - 600)
    end = min(len(c), m.end() + 200)
    print(c[start:end])
    print('---')
    print(f'pos: {m.start()}')
else:
    print('NOT FOUND in dist/index.html')
