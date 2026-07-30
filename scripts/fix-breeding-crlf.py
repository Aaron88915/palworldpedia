#!/usr/bin/env python3
import re
# 把 breeding/index.astro 转为 LF
f = 'src/pages/breeding/index.astro'
raw = open(f, 'rb').read()
lf = raw.replace(b'\r\n', b'\n')
with open(f, 'wb') as out:
    out.write(lf)
print(f'{f}: converted CRLF -> LF')
print(f'before: {len(raw)} bytes, {raw.count(b"\\r\\n")} CRLF lines')
print(f'after: {len(lf)} bytes, {lf.count(b"\\r\\n")} CRLF lines')
