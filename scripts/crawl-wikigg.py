"""
Crawl palworld.wiki.gg individual tech pages and save to a folder.
Cloudflare might block; we try with realistic browser headers + retries.
"""
import urllib.request, urllib.error, json, time, os, sys, socket
from html import unescape

socket.setdefaulttimeout(30)

OUT_DIR = r'C:\Users\31963\Desktop\palwiki-pages'
URL_LIST = r'D:\minamax\projects\palworldpedia\scripts\wikigg-technology.html'
BASE = 'https://palworld.wiki.gg/wiki/'

os.makedirs(OUT_DIR, exist_ok=True)

# Realistic browser headers to avoid Cloudflare
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'TE': 'trailers',
}

# Accept-Encoding 'gzip' requires us to decompress; let's remove to keep simple
HEADERS.pop('Accept-Encoding', None)

def fetch(url, retries=3):
    for attempt in range(1, retries + 1):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            r = urllib.request.urlopen(req, timeout=30)
            return r.read().decode('utf-8', errors='ignore'), r.status
        except urllib.error.HTTPError as e:
            if e.code in (403, 503):
                wait = 30 * attempt
                print(f'  [{attempt}/{retries}] {e.code} - waiting {wait}s...')
                time.sleep(wait)
            else:
                return None, e.code
        except Exception as e:
            print(f'  [{attempt}/{retries}] {type(e).__name__}: {e}')
            time.sleep(5 * attempt)
    return None, 0

def safe_name(name):
    """Sanitize a wiki page name to a safe Windows filename."""
    return name.replace('?', '_').replace('&', '_').replace('=', '_').replace(':', '_').replace('/', '_').replace('\\', '_').replace('"', '_').replace("'", '').replace('*', '_').replace('<', '_').replace('>', '_').replace('|', '_')[:200]

# Step 1: extract wiki page names from overview HTML
print('=== Loading overview page list ===')
with open(URL_LIST, 'r', encoding='utf-8') as f:
    html = f.read()

# Match /wiki/Name patterns
import re
names = sorted(set(re.findall(r'href="https://palworld\.wiki\.gg/wiki/([^"#]+)"', html)))
# Filter out non-tech pages (game versions, general topics, etc.)
SKIP = {
    '0.1.2.0', '0.2.0.6', '0.3.1.0', '0.3.4.0', '0.7.0', '1.0',  # versions
    'Active_Skills', 'Alpha_Pal', 'Alpha_Pals', 'Ancient_Technology',
    'Armor', 'Base', 'Bosses', 'Breeding', 'Category:Palworld_Wiki',
    'Consumables', 'Crafting', 'Dungeons', 'Elements', 'Factions',
    'Factory', 'Farming', 'Fishing', 'Ingredients', 'Items',
    'Key_Items', 'Lucky_Pals', 'Materials', 'Mounts', 'Palpedia',
    'Partner_Skills', 'Passive_Skills', 'Pals', 'Technology',  # overview page itself
    'Weapons', 'Work_Suitability', 'World', 'Breeding_Combinations',
    'Changelog', 'Game_Updates', 'Maintenance', 'Templates',
    'Tools', 'What_links_here', 'Recent_changes', 'Random_page',
    'Special:RecentChanges', 'Special:Search', 'Help:Contents',
    'Palpagos_Islands', 'Sakurajima', 'Mounts',
}
tech_names = [n for n in names if n not in SKIP and not n.startswith(('Category:', 'Special:', 'File:', 'Template:', 'Help:'))]

print(f'Total wiki pages: {len(names)}')
print(f'Tech pages to fetch: {len(tech_names)}')

# Step 2: fetch each
print(f'\n=== Fetching to {OUT_DIR} ===')
ok, fail, skip = 0, 0, 0
for i, name in enumerate(tech_names):
    outfile = os.path.join(OUT_DIR, f'{safe_name(name)}.html')
    if os.path.exists(outfile) and os.path.getsize(outfile) > 1000:
        skip += 1
        continue
    url = BASE + name
    body, status = fetch(url, retries=2)
    try:
        if body and len(body) > 1000:
            with open(outfile, 'w', encoding='utf-8') as f:
                f.write(body)
            ok += 1
        else:
            fail += 1
            # Save marker for failures
            with open(outfile, 'w', encoding='utf-8') as f:
                f.write('')
    except OSError as e:
        print(f'  OSError for {name!r}: {e}')
        fail += 1
    if (i + 1) % 10 == 0:
        print(f'[{i+1}/{len(tech_names)}] ok={ok} fail={fail} skip={skip}')
    # Polite delay
    time.sleep(1.5)

print(f'\nDone. ok={ok} fail={fail} skip={skip}')
print(f'Files in: {OUT_DIR}')
