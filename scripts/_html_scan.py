# -*- coding: utf-8 -*-
import re
html = open('scripts/_full_Kingpaca.html', encoding='utf-8').read()
ids = re.findall(r'data-pal-id="([^"]+)"', html)
print('pal ids:', ids[:20])
for m in re.finditer(r'<a href="([^"]+)"', html):
    h = m.group(1)
    if any(k in h.lower() for k in ['palbox', 'spawn', 'recruiter', 'island', 'mountain', 'forest', 'grass', 'dark', 'desert', 'sky', 'moon', 'cave', 'realm', 'sanctuary', 'palpagos']):
        print('href:', h)
print()
# Try a different page that we know works (Sibelyx)
print('=== Sibelyx hrefs ===')
html2 = open('scripts/_full_Sibelyx.html', encoding='utf-8').read()
for m in re.finditer(r'<a href="([^"]+)"', html2):
    h = m.group(1)
    if any(k in h.lower() for k in ['palbox', 'spawn', 'recruiter', 'island', 'mountain', 'forest', 'grass', 'dark', 'desert', 'sky', 'moon', 'cave', 'realm', 'sanctuary', 'palpagos']):
        print('href:', h)
