import re
with open(r'C:\Users\31963\Desktop\palwiki-pages\Palbox.html', 'r', encoding='utf-8') as f:
    h = f.read()
for kw in ['Material', 'Requirement', 'Ingredient', 'Cost', 'Recipe', 'Paldium', 'Wood']:
    idx = h.find(kw)
    if idx > 0:
        ctx = re.sub(r'\s+', ' ', h[max(0,idx-100):idx+400])
        print(f'{kw}: {ctx[:400]}')
        print('---')
