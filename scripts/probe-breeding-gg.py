# -*- coding: utf-8 -*-
"""Probe palworld.gg breeding-calculator for design/data ideas."""
import urllib.request, re

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

for url in [
    'https://palworld.gg/breeding-calculator',
    'https://palworld.gg/breeding',
    'https://palworld.gg/breeding-calculator/',
]:
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        r = urllib.request.urlopen(req, timeout=15)
        data = r.read().decode('utf-8', errors='ignore')
        print(f'\n=== {url} (status={r.status}, len={len(data)}) ===')
        title = re.search(r'<title>([^<]+)</title>', data)
        if title:
            print(f'  Title: {title.group(1)}')
        desc = re.search(r'<meta name="description" content="([^"]+)"', data)
        if desc:
            print(f'  Desc: {desc.group(1)[:300]}')
        # Look for select/dropdown options showing how they list pals
        selects = re.findall(r'<select[^>]*>(.*?)</select>', data, re.DOTALL)
        for i, s in enumerate(selects[:3]):
            opts = re.findall(r'<option[^>]*value="([^"]*)"[^>]*>([^<]+)</option>', s)
            print(f'  Select {i+1}: {len(opts)} options, first 3:')
            for v, t in opts[:3]:
                print(f'    {v} -> {t.strip()[:30]}')
        # Find any data table or result list
        tables = re.findall(r'<table[^>]*>(.*?)</table>', data, re.DOTALL)
        print(f'  Tables: {len(tables)}')
        # Find any breeding-related words
        for kw in ['shortest', 'path', 'chain', 'BFS', 'reverse', 'forward', 'tree', 'graph']:
            if kw.lower() in data.lower():
                idx = data.lower().find(kw.lower())
                ctx = data[max(0, idx-50):idx+200]
                # Strip HTML
                ctx = re.sub(r'<[^>]+>', ' ', ctx)
                ctx = re.sub(r'\s+', ' ', ctx).strip()
                print(f'  Found "{kw}": {ctx[:200]}')
                break
    except Exception as e:
        print(f'{url}: ERR {e}')
