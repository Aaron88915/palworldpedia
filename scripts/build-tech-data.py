import os, re, json
from html import unescape

# Load list data
with open('scripts/raw-tech-list.json', 'r', encoding='utf-8') as f:
    techs = json.load(f)

# Parse detail pages for enrichment
def parse(html):
    if not html or len(html) < 5000:
        return None
    out = {}
    m = re.search(r'<title>([^<]+?)\s*-\s*Palworld', html)
    if m: out['name'] = unescape(m.group(1).strip())
    m = re.search(r'<meta property="og:description" content="([^"]+)"', html)
    if m: out['description'] = unescape(m.group(1).strip())
    m = re.search(r'<meta property="og:image" content="([^"]+)"', html)
    if m: out['image'] = m.group(1).strip()
    table_match = re.search(r'<th[^>]*>\s*Materials[\s\S]{0,10000}?</table>', html, re.IGNORECASE)
    if table_match:
        table_html = table_match.group(0)
        pairs = re.findall(
            r'<a[^>]+class="itemname"[^>]*>(?:<img[^>]+/?>)?\s*([^<]+?)\s*</a>[\s\S]*?<small[^>]+class="itemQuantity"[^>]*>(\d+)</small>',
            table_html, re.IGNORECASE
        )
        if pairs:
            out['materials'] = [{'name': unescape(n.strip()), 'count': int(c)} for n, c in pairs]
        cells = re.findall(r'<td[^>]*>([\s\S]*?)(?=<td|</tr>|</table>)', table_html, re.IGNORECASE)
        if len(cells) >= 2:
            prod = re.sub(r'<[^>]+>', '', cells[1]).strip()
            if prod: out['product'] = prod
        if len(cells) >= 3:
            schem = re.sub(r'<[^>]+>', '', cells[2]).strip()
            m = re.search(r'Technology\s+(\d+)', schem, re.IGNORECASE)
            if not m: m = re.search(r'Lv\.?\s*(\d+)', schem, re.IGNORECASE)
            if m: out['unlockLevel'] = int(m.group(1))
    if 'unlockLevel' not in out:
        m = re.search(r'Technology\s+(\d+)', html)
        if m: out['unlockLevel'] = int(m.group(1))
    body_match = re.search(r'<main([\s\S]*?)</main>', html, re.IGNORECASE)
    body = body_match.group(1) if body_match else html
    text = re.sub(r'<script[\s\S]*?</script>', '', body)
    text = re.sub(r'<style[\s\S]*?</style>', '', text)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    m = re.search(r'Defense\s+(\d+)', text)
    if m: out['defense'] = int(m.group(1))
    m = re.search(r'\bHp\s+(\d+)', text)
    if m: out['hp'] = int(m.group(1))
    return out

# Enrich from downloaded detail pages
enriched = 0
enriched_data = {}
HTML_DIR = 'scripts/paldb-tech-html'
for t in techs:
    slug = t['slug']
    path = os.path.join(HTML_DIR, f'{slug}.html')
    if os.path.exists(path) and os.path.getsize(path) > 5000:
        with open(path, 'r', encoding='utf-8') as f:
            html = f.read()
        data = parse(html)
        if data:
            enriched_data[slug] = data
            enriched += 1

print(f'Enriched {enriched} techs from detail pages')

# Merge
for t in techs:
    if t['slug'] in enriched_data:
        ed = enriched_data[t['slug']]
        # Prefer enriched data
        if 'description' in ed: t['description'] = ed['description']
        if 'image' in ed: t['image'] = ed['image']
        if 'materials' in ed: t['materials'] = ed['materials']
        if 'product' in ed: t['product'] = ed['product']
        if 'unlockLevel' in ed: t['unlockLevel'] = ed['unlockLevel']
        if 'defense' in ed: t['defense'] = ed['defense']
        if 'hp' in ed: t['hp'] = ed['hp']

# Add id (slug-based)
for i, t in enumerate(techs):
    t['id'] = t['slug'].lower()

# Save
out_path = 'src/data/tech.json'
os.makedirs('src/data', exist_ok=True)
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(techs, f, ensure_ascii=False, indent=1)
print(f'Saved {len(techs)} techs to {out_path}')

# Stats
from collections import Counter
cats = Counter(t['category'] for t in techs)
print('Categories:', dict(cats))
with_desc = sum(1 for t in techs if 'description' in t)
with_mat = sum(1 for t in techs if 'materials' in t)
print(f'With description: {with_desc}')
print(f'With materials: {with_mat}')
