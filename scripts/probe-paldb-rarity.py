# -*- coding: utf-8 -*-
"""Probe paldb.cc for rarity field."""
import urllib.request, re

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

for slug in ['Jetragon', 'Lamball', 'Frostallion-Noct', 'Panthalus', 'Mau', 'Cattiva']:
    url = f'https://paldb.cc/en/{slug}'
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        r = urllib.request.urlopen(req, timeout=20)
        d = r.read().decode('utf-8', errors='ignore')
        print(f'\n=== {slug} (len={len(d)}) ===')
        # Look for rarity mentions
        for kw in ['Rarity', 'rarity', 'Legendary', 'Epic', 'Rare', 'Common', 'Paldeck', 'No.']:
            for m in re.finditer(rf'[\s>]({re.escape(kw)}[^<>"\n]{{0,80}})', d):
                ctx = m.group(1)[:120]
                print(f'  [{kw}]: {ctx}')
                break
    except Exception as e:
        print(f'  {slug}: ERR {e}')
