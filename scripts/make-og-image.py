#!/usr/bin/env python3
"""生成 og-image.png 分享卡（1200x630，符合 OG/Twitter 规范）"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630
OUT = 'public/og-image.png'

# 配色（与 favicon 一致）
BG = (15, 20, 25)
PEAK_TOP = (245, 166, 35)
PEAK_BOT = (139, 105, 20)
TEXT = (245, 245, 245)
MUTED = (180, 180, 180)
ACCENT = (251, 191, 36)

# 字体
FONT_PATHS = [
    r'C:\Windows\Fonts\msyh.ttc',
    r'C:\Windows\Fonts\msyh.ttf',
    r'C:\Windows\Fonts\msyhbd.ttc',
    r'C:\Windows\Fonts\simhei.ttf',
    r'C:\Windows\Fonts\simsun.ttc',
    r'C:\Windows\Fonts\arial.ttf',
    r'C:\Windows\Fonts\segoeui.ttf',
]
def load_font(size, bold=False):
    for p in FONT_PATHS:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except:
                pass
    return ImageFont.load_default()

font_huge = load_font(96, True)
font_big = load_font(72, True)
font_med = load_font(48, False)
font_small = load_font(36, False)

img = Image.new('RGB', (W, H), BG)
draw = ImageDraw.Draw(img)

# 背景：渐变圆点（左上 + 右下）
import random
random.seed(42)
for _ in range(60):
    cx = random.randint(0, W)
    cy = random.randint(0, H)
    r = random.randint(80, 200)
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    alpha = random.randint(8, 20)
    color = PEAK_TOP if random.random() > 0.5 else (94, 179, 245)
    od.ellipse([cx-r, cy-r, cx+r, cy+r], fill=color + (alpha,))
    img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
    draw = ImageDraw.Draw(img)

# 装饰几何（右侧大圆 + 山峰）
# 大橙色圆
draw.ellipse([W-300, -100, W+100, 300], fill=PEAK_BOT)
# 山峰
sx, sy = 880, 100
peak = [
    (sx, sy),
    (sx+200, sy+200),
    (sx+170, sy+200),
    (sx+170, sy+460),
    (sx+30, sy+460),
    (sx+30, sy+200),
    (sx, sy+200),
]
draw.polygon(peak, fill=PEAK_TOP)
draw.ellipse([sx+85, sy+330, sx+115, sy+360], fill=BG)

# 左侧 LOGO 区
# ⚡ 符号（用梯形 + 圆点示意）
logox, logoy = 80, 80
# 圆形底
draw.ellipse([logox, logoy, logox+80, logoy+80], fill=PEAK_TOP)
# ⚡ 白色简化版
import math
def draw_bolt(d, x, y, size=50, color=(255, 255, 255)):
    s = size
    pts = [
        (x + 0.6*s, y),
        (x, y + 0.6*s),
        (x + 0.4*s, y + 0.6*s),
        (x + 0.4*s, y + s),
        (x + s, y + 0.4*s),
        (x + 0.6*s, y + 0.4*s),
        (x + 0.6*s, y),
    ]
    d.polygon(pts, fill=color)
draw_bolt(draw, logox+15, logoy+15, 50, (255, 255, 255))

# 标题 "Palworldpedia"
draw.text((80, 200), 'Palworldpedia', font=font_huge, fill=TEXT)

# 中文副标题
draw.text((80, 310), '幻兽帕鲁最全攻略站', font=font_big, fill=PEAK_TOP)

# 数据亮点（3 个 metric）
metrics = [
    ('288', '只帕鲁图鉴'),
    ('40,972', '条配种公式'),
    ('587', '个科技点'),
]
mx = 80
my = 450
for i, (num, label) in enumerate(metrics):
    cx = mx + i * 360
    # 大数字
    draw.text((cx, my), num, font=font_big, fill=ACCENT)
    # 标签
    draw.text((cx, my + 90), label, font=font_small, fill=MUTED)

# 底部 URL
draw.text((80, H-50), 'palworldpedia.cc', font=font_small, fill=MUTED)

# 右侧小标签
draw.text((W-280, H-50), 'Updated 2026', font=font_small, fill=MUTED)

img.save(OUT, 'PNG', optimize=True)
size = os.path.getsize(OUT)
print(f'Generated: {OUT}  ({size} bytes, {W}x{H})')
