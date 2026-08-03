# -*- coding: utf-8 -*-
"""Probe paldb.cc HTML to understand biome section."""
import urllib.request, re

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

# Try a few names
for name in ['Kingpaca', 'Flopie', 'Fenglope', 'Grizzbolt', 'Orserk', 'Bellanoir', 'Jetragon', 'Paladius', 'Necromus', 'Frostallion', 'Sibelyx', 'Loupmoon']:
    url = 'https://paldb.cc/en/' + name
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        r = urllib.request.urlopen(req, timeout=20)
        html = r.read().decode('utf-8', errors='ignore')
        # find Pal Recruiter section
        m = re.search(r'Pal Recruiter.{0,5000}', html, re.DOTALL)
        snippet = ''
        if m:
            text = re.sub(r'<[^>]+>', ' ', m.group(0))
            text = re.sub(r'\s+', ' ', text)
            snippet = text[:600]
        # Also look for any %-marked items
        items = re.findall(r'([A-Za-z_]+)\s+\d+\.?\d*%', snippet)
        # Also look for known biome-like tokens
        open('scripts/_probe_%s.txt' % name, 'w', encoding='utf-8').write(snippet)
        print('%s: %d%%-items, snippet saved' % (name, len(items)))
    except Exception as e:
        print('%s: ERR %s' % (name, e))
