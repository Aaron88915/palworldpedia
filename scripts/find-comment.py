#!/usr/bin/env python3
import re
files = [
    'dist/index.html',
    'dist/pals/index.html',
    'dist/breeding/index.html',
    'dist/tech-tree/index.html',
    'dist/about/index.html',
]
for f in files:
    c = open(f, encoding='utf-8').read()
    comment = '广告位' in c
    inline_comment = '广告位 #1' in c
    print(f'{f:<40} 广告位 in HTML: {comment}  广告位 #1: {inline_comment}')
    if '广告位 #1' in c:
        idx = c.find('广告位 #1')
        print(f'    context: ...{c[max(0,idx-30):idx+50]}...')
