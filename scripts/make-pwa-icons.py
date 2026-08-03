#!/usr/bin/env python3
"""生成 PWA 用的 192x192 和 512x512 图标"""
from PIL import Image
import os
src = 'public/favicon-256.png'
for size in [192, 512]:
    img = Image.open(src)
    out = f'public/favicon-{size}.png'
    img.resize((size, size), Image.LANCZOS).save(out, 'PNG', optimize=True)
    print(f'{out}: {os.path.getsize(out)} bytes')
