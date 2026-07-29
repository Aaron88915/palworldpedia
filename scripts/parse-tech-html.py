import os, re, json
from html import unescape

def parse(html):
    """Extract tech fields from paldb.cc detail page."""
    if not html or len(html) < 2000:
        return None
    out = {}

    # 1. Title
    m = re.search(r'<title>([^<]+?)\s*-\s*Palworld', html)
    if m:
        out['name'] = unescape(m.group(1).strip())

    # 2. Description (og:description)
    m = re.search(r'<meta property="og:description" content="([^"]+)"', html)
    if m:
        out['description'] = unescape(m.group(1).strip())

    # 3. Image (og:image)
    m = re.search(r'<meta property="og:image" content="([^"]+)"', html)
    if m:
        out['image'] = m.group(1).strip()

    # 4. Find the Materials table
    # Look for the <table> after a header that mentions "Materials"
    # The paldb.cc table has: <th>Materials<th>Product<th>Schematic (all on one line, may have attributes)
    table_match = re.search(
        r'<th[^>]*>\s*Materials[\s\S]{0,10000}?</table>',
        html, re.IGNORECASE
    )
    if table_match:
        table_html = table_match.group(0)

        # Extract all (itemname, itemQuantity) pairs
        pairs = re.findall(
            r'<a[^>]+class="itemname"[^>]*>(?:<img[^>]+/?>)?\s*([^<]+?)\s*</a>[\s\S]*?<small[^>]+class="itemQuantity"[^>]*>(\d+)</small>',
            table_html, re.IGNORECASE
        )
        if pairs:
            out['materials'] = [{'name': unescape(n.strip()), 'count': int(c)} for n, c in pairs]

        # Product: content of 2nd <td>
        # Note: paldb.cc uses <td>X<td>Y<td>Z without </td> between cells
        cells = re.findall(r'<td[^>]*>([\s\S]*?)(?=<td|</tr>|</table>)', table_html, re.IGNORECASE)
        if len(cells) >= 2:
            prod = re.sub(r'<[^>]+>', '', cells[1]).strip()
            if prod:
                out['product'] = prod
        if len(cells) >= 3:
            schem = re.sub(r'<[^>]+>', '', cells[2]).strip()
            m = re.search(r'Technology\s+(\d+)', schem, re.IGNORECASE)
            if not m:
                m = re.search(r'Lv\.?\s*(\d+)', schem, re.IGNORECASE)
            if m:
                out['unlockLevel'] = int(m.group(1))

    # 5. Fallback unlockLevel from text "Technology N" if not yet found
    if 'unlockLevel' not in out:
        m = re.search(r'Technology\s+(\d+)', html)
        if m:
            out['unlockLevel'] = int(m.group(1))

    # 6. Stats (HP, Defense) - look in body text
    body_match = re.search(r'<main([\s\S]*?)</main>', html, re.IGNORECASE)
    body = body_match.group(1) if body_match else html
    text = re.sub(r'<script[\s\S]*?</script>', '', body)
    text = re.sub(r'<style[\s\S]*?</style>', '', text)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text)

    m = re.search(r'Defense\s+(\d+)', text)
    if m:
        out['defense'] = int(m.group(1))
    m = re.search(r'\bHp\s+(\d+)', text)
    if m:
        out['hp'] = int(m.group(1))

    return out


# Test on Palbox
with open('scripts/paldb-palbox.html', 'r', encoding='utf-8') as f:
    html = f.read()
data = parse(html)
print('=== Palbox ===')
for k, v in (data or {}).items():
    print(f'  {k}: {v}')
