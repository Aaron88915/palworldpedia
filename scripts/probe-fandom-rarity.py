# -*- coding: utf-8 -*-
"""Probe Fandom wiki - use query API (different endpoint)."""
import urllib.request, re, json

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.5',
}

def get_wikitext(title):
    url = f'https://palworld.fandom.com/api.php?action=query&prop=revisions&titles={urllib.parse.quote(title)}&format=json&rvprop=content&rvslots=main'
    req = urllib.request.Request(url, headers=HEADERS)
    r = urllib.request.urlopen(req, timeout=20)
    j = json.loads(r.read())
    pages = j.get('query', {}).get('pages', {})
    for pid, p in pages.items():
        revs = p.get('revisions', [])
        if revs:
            return revs[0].get('slots', {}).get('main', {}).get('*', '')
    return ''

import urllib.parse

for title in ['Jetragon', 'Lamball', 'Cattiva', 'Frostallion Noct', 'Panthalus', 'Rayhound', 'Mau']:
    try:
        wt = get_wikitext(title)
        print(f'\n=== {title} (len={len(wt)}) ===')
        # Search for rarity / Rarity
        for kw in ['Rarity', 'rarity', 'rarityIcon', 'Legendary', 'Common', 'Rare', 'Epic']:
            if kw in wt:
                idx = wt.find(kw)
                ctx = wt[max(0,idx-50):idx+200]
                ctx = re.sub(r'\n+', ' ', ctx)
                print(f'  [{kw}]: {ctx[:300]}')
                break
    except Exception as e:
        print(f'  {title}: ERR {e}')
