import re
with open('dist/tech-tree/index.html', 'r', encoding='utf-8') as f:
    html = f.read()
cards = re.findall(r'class="tech-card"', html)
print(f'Tech cards: {len(cards)}')
idx = html.find('class="tech-card"')
if idx > 0:
    print('First card context:')
    print(html[idx:idx+500])
