#!/usr/bin/env python3
import re
for f in ['dist/index.html', 'dist/en/index.html']:
    print(f'=== {f} ===')
    c = open(f, encoding='utf-8').read()
    for m in re.finditer(r'<link[^>]*rel="canonical"[^>]*>|<link[^>]*hreflang[^>]*>|<meta[^>]*name="description"[^>]*>', c):
        print(' ', m.group(0))
    print()
