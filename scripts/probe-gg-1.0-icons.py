import re
with open('scripts/gg-techtree.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Try alternate names
queries = ['Dresser', 'Altar', 'Incubator', 'Generator', 'Hatchery', 'Wing', 'Summon']
for q in queries:
    matches = list(re.finditer(re.escape(q), html, re.IGNORECASE))
    print(f'\n{q}: {len(matches)} hits')
    for m in matches[:3]:
        idx = m.start()
        ctx = re.sub(r'\s+', ' ', html[max(0,idx-200):idx+300])
        print(f'  @{idx}: {ctx[:400]}')
