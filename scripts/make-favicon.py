#!/usr/bin/env python3
"""生成 favicon.ico (多分辨率) + apple-touch-icon.png
设计：黑底 (#0f1419) + 橙色山峰 (#f5a623 → #8b6914 渐变) + 中心点
"""
from PIL import Image, ImageDraw
import os

OUT_DIR = 'public'

# 设计参数
BG = (15, 20, 25)        # #0f1419
PEAK_TOP = (245, 166, 35)  # #f5a623
PEAK_BOT = (139, 105, 20)  # #8b6914
ACCENT = BG

def make_icon(size: int) -> Image.Image:
    """生成一个 size×size 的图标"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 圆角矩形底
    r = max(2, size // 6)  # 圆角半径
    draw.rounded_rectangle(
        [(0, 0), (size - 1, size - 1)],
        radius=r,
        fill=BG
    )

    # 山峰 (三角形)：底部 2 个尖端 + 顶部 1 个尖端
    # 模拟 SVG: M32 8 L48 24 L40 24 L40 48 L24 48 L24 24 L16 24 Z
    s = size / 64.0  # 缩放比例
    pts = [
        (32 * s, 8 * s),     # 顶点
        (48 * s, 24 * s),    # 右外
        (40 * s, 24 * s),    # 右内
        (40 * s, 48 * s),    # 右下
        (24 * s, 48 * s),    # 左下
        (24 * s, 24 * s),    # 左内
        (16 * s, 24 * s),    # 左外
    ]
    # 用渐变（手动用单色简化，ICO 不支持渐变）
    # 上半用 PEAK_TOP，下半用 PEAK_BOT
    # 简单做法：整个山峰用单一橙色（gradient 在 ICO 缩略图看不出来）
    draw.polygon(pts, fill=PEAK_TOP)

    # 中心点（在山峰内）
    cx, cy = 32 * s, 36 * s
    rad = max(1, int(3 * s))
    draw.ellipse(
        [(cx - rad, cy - rad), (cx + rad, cy + rad)],
        fill=ACCENT
    )

    return img

# 生成多分辨率 PNG
sizes = [16, 32, 48, 64, 128, 256]
images = {s: make_icon(s) for s in sizes}

# 保存 PNG 备份
for s, img in images.items():
    img.save(os.path.join(OUT_DIR, f'favicon-{s}.png'))

# 主 favicon.ico 多分辨率
ico_path = os.path.join(OUT_DIR, 'favicon.ico')
images[256].save(
    ico_path,
    format='ICO',
    sizes=[(s, s) for s in [16, 32, 48, 64, 128, 256]]
)

# Apple touch icon 180x180
apple = make_icon(180)
apple.save(os.path.join(OUT_DIR, 'apple-touch-icon.png'))

# OG image / default 也顺便做个 512x512（如果需要）
og = make_icon(512)
og.save(os.path.join(OUT_DIR, 'icon-512.png'))

# 输出
print('Generated:')
for f in ['favicon.ico', 'favicon-16.png', 'favicon-32.png', 'favicon-48.png',
          'favicon-64.png', 'favicon-128.png', 'favicon-256.png',
          'apple-touch-icon.png', 'icon-512.png']:
    path = os.path.join(OUT_DIR, f)
    if os.path.exists(path):
        print(f'  {f:<30} {os.path.getsize(path)} bytes')
