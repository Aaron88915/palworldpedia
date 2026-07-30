#!/usr/bin/env python3
import re
c = open('dist/breeding/index.html', encoding='utf-8').read()
# 找所有 "完整配种表" 出现
matches = list(re.finditer(r'完整配种表', c))
print(f'Found {len(matches)} matches')
for i, m in enumerate(matches):
    pos = m.start()
    start = max(0, pos - 800)
    end = min(len(c), pos + 200)
    snippet = c[start:end]
    snippet = re.sub(r'>\s*<', '>\n<', snippet)
    print(f'\n=== match #{i+1} @ {pos} ===')
    # 只显示最后 200 字符
    print(snippet[-1200:])
