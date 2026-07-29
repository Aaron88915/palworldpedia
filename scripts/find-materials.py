import re
with open('scripts/paldb-palbox.html', 'r', encoding='utf-8') as f:
    html = f.read()
m = re.search(r'<th[^>]*>Materials[\s\S]{0,5000}?</table>', html, re.IGNORECASE)
if m:
    table = m.group(0)
    print('Table HTML (first 1500 chars):')
    print(table[:1500])
    print('---')
    pairs = re.findall(
        r'<a[^>]+class="itemname"[^>]*>(?:<img[^>]+/?>)?\s*([^<]+?)\s*</a>[\s\S]*?<small[^>]+class="itemQuantity"[^>]*>(\d+)</small>',
        table, re.IGNORECASE
    )
    print('Pairs found:', pairs)
