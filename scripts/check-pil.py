#!/usr/bin/env python3
try:
    from PIL import Image, ImageDraw
    print('PIL ok')
except ImportError as e:
    print(f'PIL missing: {e}')
