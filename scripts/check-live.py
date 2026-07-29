# -*- coding: utf-8 -*-
"""Check if combo CSS rule is live on palworldpedia.cc."""
import urllib.request, re

r = urllib.request.urlopen('https://palworldpedia.cc', timeout=15)
d = r.read().decode('utf-8', errors='ignore')
css_links = re.findall(r'href="(/_astro/[^"]+\.css)"', d)
print(f'CSS files: {css_links}')
print()

for css in css_links:
    try:
        r2 = urllib.request.urlopen(f'https://palworldpedia.cc{css}', timeout=15)
        css_d = r2.read().decode('utf-8', errors='ignore')
        if 'combo-parent' in css_d and 'pal-image-wrap' in css_d:
            # Find the combo rule
            idx = css_d.find('combo-parent')
            ctx = css_d[max(0, idx-50):idx+300]
            print(f'{css}: COMBO RULE LIVE')
            print(f'  {ctx[:250]}')
        else:
            print(f'{css}: no combo rule')
    except Exception as e:
        print(f'{css}: ERR {e}')
