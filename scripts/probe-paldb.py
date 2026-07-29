# -*- coding: utf-8 -*-
import urllib.request, json, re

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

for url in [
    'https://paldb.cc/en/Lamball',
    'https://paldb.cc/en/Cattiva',
    'https://paldb.cc/en/Gumoss',
]:
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        r = urllib.request.urlopen(req, timeout=15)
        data = r.read().decode('utf-8', errors='ignore')
        print(f'=== {url} (len={len(data)}) ===')
        # Look for app/data
        json_data = re.findall(r'window\.__[A-Z_]+__\s*=\s*(\{[^;]*\});', data)
        if json_data:
            for j in json_data[:2]:
                print(f'  Found window.__*__ data, {len(j)} chars')
                if 'Windswept' in j or 'biome' in j.lower():
                    idx = max(j.find('Windswept'), j.lower().find('biome'))
                    print(f'  ...{j[max(0,idx-100):idx+300]}...')
        # Look for inline JSON
        for pat in [r'"biome[s]?":\s*\[([^\]]*)\]', r'"spawnLocation":\s*\[([^\]]*)\]']:
            ms = re.findall(pat, data)
            if ms:
                print(f'  Pattern {pat}: {ms[0][:200]}')
        # Find any 1.0 biome names
        for nm in ['Windswept Island', 'Sea Breeze', 'Marsh Island', 'Eastern Wild', 'Isle of Murmurs']:
            if nm in data:
                print(f'  Has "{nm}"')
        # Find "Isle of Silence"
        for nm in ['Isle of Silence', 'Feybreak', 'Sakurajima']:
            if nm in data:
                print(f'  Has "{nm}"')
    except Exception as e:
        print(f'{url}: ERR {str(e)[:100]}')
    print()
