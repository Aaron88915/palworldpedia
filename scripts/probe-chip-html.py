import re
html = open('dist/pals/index.html', encoding='utf-8').read()
m = re.search(r'<button[^>]*class="chip type-chip type-fire"[^>]*>[^<]*</button>', html)
print('Fire chip:', m.group(0) if m else 'NOT FOUND')
m2 = re.search(r'<button[^>]*class="chip type-chip type-ground"[^>]*>[^<]*</button>', html)
print('Ground chip:', m2.group(0) if m2 else 'NOT FOUND')
m3 = re.search(r'<button[^>]*class="chip type-chip type-dark"[^>]*>[^<]*</button>', html)
print('Dark chip:', m3.group(0) if m3 else 'NOT FOUND')
