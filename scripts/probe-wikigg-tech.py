import re
with open('scripts/wikigg-technology.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find all wiki page links
wiki_links = set(re.findall(r'href="https://palworld\.wiki\.gg/wiki/([^"#]+)"', html))
print(f'Unique wiki page links: {len(wiki_links)}')
for link in sorted(wiki_links)[:30]:
    print(f'  {link}')
print('...')
for link in sorted(wiki_links)[-10:]:
    print(f'  {link}')

# Compare to our tech names
import json
with open('src/data/tech.json', 'r', encoding='utf-8') as f:
    techs = json.load(f)
our_slugs = {t['name'].replace(' ', '_') for t in techs}
our_slugs |= {t['name'].replace("'", '').replace(' ', '_') for t in techs}

# Match
matched = wiki_links & our_slugs
print(f'\nMatched: {len(matched)}/{len(wiki_links)}')
unmatched = wiki_links - our_slugs
print(f'Unmatched wiki links: {len(unmatched)}')
for u in sorted(unmatched)[:20]:
    print(f'  {u}')
