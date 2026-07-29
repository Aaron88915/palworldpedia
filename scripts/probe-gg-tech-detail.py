import re, os
# Look for technology-related data in the pal data bundle
path = 'scripts/palworldgg-bundles/CK2A4_hG.js'
with open(path, 'r', encoding='utf-8', errors='ignore') as f:
    c = f.read()

# Find technology sections
for kw in ['technology', 'Technology', 'techTree', 'TechTree', 'recipe', 'Recipe', 'TechCost', 'techCost', 'Ancient']:
    count = c.count(kw)
    print(f'{kw}: {count} hits')

# Find "Technology" with surrounding context
print()
print('=== Technology context ===')
matches = list(re.finditer(r'[Tt]echnology', c))
for m in matches[:3]:
    idx = m.start()
    print(f'@{idx}:', re.sub(r'\s+', ' ', c[max(0,idx-80):idx+200]))
    print('---')
