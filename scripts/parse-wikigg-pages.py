"""
Parse the wiki.gg pages we downloaded and extract tech data.
Outputs JSON with all extracted fields, ready to merge into tech.json.
"""
import os, re, json
from html import unescape

DIR = r'C:\Users\31963\Desktop\palwiki-pages'

def parse(html):
    """Extract description + materials + image from a wiki.gg tech page."""
    if not html or len(html) < 2000:
        return None
    out = {}

    # 1. Title (og:title or first h1)
    m = re.search(r'<meta property="og:title" content="([^"]+)"', html)
    if m:
        out['name'] = unescape(m.group(1).strip())
    else:
        m = re.search(r'<h1[^>]*>([^<]+)</h1>', html)
        if m:
            out['name'] = unescape(m.group(1).strip())

    # 2. Description
    m = re.search(r'<meta property="og:description" content="([^"]+)"', html)
    if m:
        out['description'] = unescape(m.group(1).strip())

    # 3. Image
    m = re.search(r'<meta property="og:image" content="([^"]+)"', html)
    if m:
        out['image'] = m.group(1).strip()

    # 4. Find content area (mw-parser-output is the standard MediaWiki content div)
    body_match = re.search(r'<div[^>]*class="mw-parser-output"[^>]*>([\s\S]*?)<div[^>]*class="printfooter"', html)
    if not body_match:
        body_match = re.search(r'<div[^>]*class="mw-parser-output"[^>]*>([\s\S]*)', html)
    body = body_match.group(1) if body_match else html

    # Strip script/style
    body = re.sub(r'<script[\s\S]*?</script>', '', body)
    body = re.sub(r'<style[\s\S]*?</style>', '', body)

    # 5. Find "Unlocks" / "Required Materials" / "Cost" sections
    # The wiki structure: <h3>Heading</h3> <p>content</p> or <table>
    # Look for the description - first <p> after the page header
    paragraphs = re.findall(r'<p>([\s\S]*?)</p>', body)
    if paragraphs:
        # Filter out empty / image-only paragraphs
        for p in paragraphs[:5]:
            text = re.sub(r'<[^>]+>', '', p).strip()
            text = re.sub(r'\s+', ' ', text)
            # Skip infobox, image-only, empty
            if len(text) > 30 and not text.startswith(('Image', 'File:')):
                if 'description' not in out:
                    out['description'] = unescape(text)
                    break

    # 6. Materials - look for table or list with item names + counts
    # Pattern: <th>Required Materials</th> or <td>Material</td><td>Count</td>
    mat_pairs = []

    # Look for a Materials table
    mat_table_match = re.search(
        r'(?:Materials|Required\s+Materials|Cost|Recipe)[\s\S]{0,5000}?</table>',
        body, re.IGNORECASE
    )
    if mat_table_match:
        mat_html = mat_table_match.group(0)
        # Extract rows with item + count
        rows = re.findall(r'<tr[^>]*>([\s\S]*?)</tr>', mat_html, re.IGNORECASE)
        for row in rows:
            # Find cells
            cells_text = re.findall(r'<t[dh][^>]*>([\s\S]*?)</t[dh]>', row, re.IGNORECASE)
            cells_clean = [re.sub(r'<[^>]+>', '', c).strip() for c in cells_text]
            # Look for pattern: name, count
            for i in range(len(cells_clean) - 1):
                name = cells_clean[i]
                count_str = cells_clean[i + 1]
                if name and count_str.isdigit():
                    if name not in ('', 'Material', 'Item', 'Materials', 'Cost', 'Count', 'Amount'):
                        mat_pairs.append({'name': unescape(name), 'count': int(count_str)})
                        break
            if mat_pairs:
                break
        if mat_pairs:
            out['materials'] = mat_pairs

    # 7. Cost / Level - look for a Cost row
    cost_match = re.search(r'(?:Cost|Technology\s+Cost|Tech\s+Point)[\s\S]{0,200}?(\d+)', body, re.IGNORECASE)
    if cost_match:
        out['cost'] = int(cost_match.group(1))

    # 8. Required Level (might be "Level 2" or "Lv 2")
    level_match = re.search(r'(?:Required\s+Level|Unlocks?\s+at|Minimum\s+Level|Level[:\s]+)(\d+)', body, re.IGNORECASE)
    if level_match:
        out['unlockLevel'] = int(level_match.group(1))

    return out


# Process all files
results = []
ok = 0
fail = 0
for fname in sorted(os.listdir(DIR)):
    if not fname.endswith('.html'):
        continue
    path = os.path.join(DIR, fname)
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    if len(html) < 2000:
        fail += 1
        continue
    data = parse(html)
    if data:
        # Use filename as the slug
        slug = fname.replace('.html', '')
        data['slug'] = slug
        results.append(data)
        ok += 1
    else:
        fail += 1

print(f'Parsed: {ok} ok, {fail} fail (probably empty/404 pages)')
print(f'Total results: {len(results)}')

# Stats
with_desc = sum(1 for r in results if r.get('description'))
with_mat = sum(1 for r in results if r.get('materials'))
with_cost = sum(1 for r in results if 'cost' in r)
with_lv = sum(1 for r in results if 'unlockLevel' in r)
print(f'With description: {with_desc}')
print(f'With materials: {with_mat}')
print(f'With cost: {with_cost}')
print(f'With unlockLevel: {with_lv}')

# Save
out_path = 'scripts/wikigg-tech-data.json'
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=1)
print(f'Saved to {out_path}')

# Show samples
print('\n=== Sample entries ===')
for r in results[:5]:
    print(f'  {r.get("name", "?")} (slug={r.get("slug")})')
    if r.get('description'):
        print(f'    desc: {r["description"][:120]}')
    if r.get('materials'):
        print(f'    mat: {r["materials"][:3]}')
    if r.get('cost'):
        print(f'    cost: {r["cost"]}')
