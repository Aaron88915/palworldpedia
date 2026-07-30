#!/usr/bin/env python3
import re, os
# 检查 dist 中每个 HTML 文件的 ad-slot 计数
results = []
for root, _, files in os.walk('dist'):
    for f in files:
        if not f.endswith('.html'):
            continue
        path = os.path.join(root, f)
        c = open(path, encoding='utf-8').read()
        top = len(re.findall(r'ad-slot-top', c))
        bottom = len(re.findall(r'ad-slot-bottom', c))
        inline = len(re.findall(r'ad-slot-inline', c))
        if top == 0 and bottom == 0 and inline == 0:
            continue
        results.append((path, top, inline, bottom))

# 统计 inline=0 的页面
no_inline = [r for r in results if r[2] == 0]
has_inline = [r for r in results if r[2] > 0]
print(f'有 inline: {len(has_inline)}')
print(f'无 inline: {len(no_inline)}')
print()
print('=== 无 inline 的页面（应该是 4 个）===')
for r in sorted(no_inline):
    print(f'  {r[0]:<60} top={r[1]} inline={r[2]} bottom={r[3]}')
print()
print('=== 有 inline 的页面（按 inline 数）===')
inline_dist = {}
for r in has_inline:
    inline_dist[r[2]] = inline_dist.get(r[2], 0) + 1
print(f'inline 分布: {inline_dist}')
