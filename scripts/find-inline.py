#!/usr/bin/env python3
import re
f = 'dist/index.html'
c = open(f, encoding='utf-8').read()
# 找 ad-slot 相关的任何字符串
for m in re.finditer(r'(ad-slot|adsbygoogle|inline)', c):
    around = c[max(0, m.start()-40):min(len(c), m.end()+80)]
    around = re.sub(r'\s+', ' ', around)
    print(f'@{m.start()}: ...{around}...')
print('---')
print('total chars:', len(c))
print('ad-slot matches:', len(re.findall(r'ad-slot', c)))
print('ad-slot-inline matches:', len(re.findall(r'ad-slot-inline', c)))
print('ad-slot-top matches:', len(re.findall(r'ad-slot-top', c)))
print('ad-slot-bottom matches:', len(re.findall(r'ad-slot-bottom', c)))
