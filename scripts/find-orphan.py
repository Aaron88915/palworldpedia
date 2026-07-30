#!/usr/bin/env python3
import re
# 检查 dist 是否有任何 ad-slot 字符串，但被错误嵌套
for f in ['dist/index.html', 'dist/pals/index.html', 'dist/breeding/index.html', 'dist/tech-tree/index.html']:
    c = open(f, encoding='utf-8').read()
    # 找 ad-slot 出现的所有位置
    matches = list(re.finditer(r'ad-slot[\w-]*', c))
    print(f'\n=== {f} ({len(matches)} matches) ===')
    for m in matches:
        # find line number
        line_num = c[:m.start()].count('\n') + 1
        # find the containing element
        before = c[max(0, m.start()-80):m.start()]
        after = c[m.end():m.end()+80]
        before = re.sub(r'\s+', ' ', before)
        after = re.sub(r'\s+', ' ', after)
        print(f'  line {line_num}: ...{before} | {m.group()} | {after[:50]}...')

# 找 ad-slot 引用
print('\n=== ad-slot all in dist ===')
import os
for root, _, files in os.walk('dist'):
    for f in files:
        if f.endswith('.html'):
            path = os.path.join(root, f)
            c = open(path, encoding='utf-8').read()
            inline = len(re.findall(r'ad-slot-inline', c))
            top = len(re.findall(r'ad-slot-top', c))
            bottom = len(re.findall(r'ad-slot-bottom', c))
            if inline > 0:
                print(f'{path}: top={top} inline={inline} bottom={bottom}')
