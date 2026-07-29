import re, json

with open('scripts/gg-techtree.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Match: <div class="item" style="background-image:url(...);">...<div class="name"><span>NAME</span>
# URL is HTML-encoded: &#39;...&amp;...&#39;
pattern = re.compile(
    r'<div class="item"\s+style="background-image:url\(&#39;([^&]+(?:&amp;[^&]+)*)&#39;\);">'
    r'.*?<div class="name"><span>([^<]+)</span></div>',
    re.DOTALL
)

mapping = {}
for m in pattern.finditer(html):
    raw_url, name = m.group(1), m.group(2).strip()
    # Decode HTML entities
    url = raw_url.replace('&amp;', '&')
    # Strip _ipx prefix to get direct URL
    direct = re.sub(r'/_ipx/[^/]+/', '/', url)
    if not name or name in mapping:
        continue
    mapping[name] = {'ipx': url, 'direct': direct}

print(f'Unique techs: {len(mapping)}')

# Save
with open('scripts/gg-tech-icon-map.json', 'w', encoding='utf-8') as f:
    json.dump(mapping, f, ensure_ascii=False, indent=1)

# Sample
for name, urls in list(mapping.items())[:5]:
    print(f'  {name}: {urls["direct"]}')

# Find missing from our tech.json
with open('src/data/tech.json', 'r', encoding='utf-8') as f:
    techs = json.load(f)
missing = [t for t in techs if t['icon'].startswith('https://cdn.paldb.cc/')]
print(f'\nMissing in our data: {len(missing)}')
matched = 0
for t in missing:
    if t['name'] in mapping:
        matched += 1
print(f'Can fill from GG: {matched}')
# Sample names not in GG
unmatched = [t['name'] for t in missing if t['name'] not in mapping]
print(f'Not in GG: {len(unmatched)}')
for n in unmatched[:10]:
    print(f'  {n}')
