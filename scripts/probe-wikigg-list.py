import re
with open('scripts/wikigg-technology.html', 'r', encoding='utf-8') as f:
    h = f.read()
names = set(re.findall(r'href="https://palworld\.wiki\.gg/wiki/([^"#]+)"', h))
print(f'Unique pages: {len(names)}')
