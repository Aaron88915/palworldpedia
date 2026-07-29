# -*- coding: utf-8 -*-
import urllib.request, json, urllib.parse, re

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36', 'Accept': 'application/json'}

# Get Lamball full content and look for location/biome/habitat patterns
title = 'Lamball'
url = f'https://palworld.fandom.com/api.php?action=query&format=json&prop=revisions&titles={urllib.parse.quote(title)}&rvprop=content&rvslots=main'
req = urllib.request.Request(url, headers=HEADERS)
j = json.loads(urllib.request.urlopen(req, timeout=15).read().decode('utf-8'))
pages = j.get('query',{}).get('pages',{})
for pid, p in pages.items():
    content = p['revisions'][0]['slots']['main']['*']
    # Find all "|" parameters in the Pal template
    params = re.findall(r'\|\s*([a-z_]+)\s*=\s*([^\n]+)', content)
    print('All Pal template params:')
    for k, v in params:
        if any(x in k.lower() for x in ['habitat','loc','biome','map','area','region','zone','place','where','find','spawn','time','day','night','noct']):
            print(f'  {k} = {v}')
    print()
    # Also look for the gallery section
    gallery = re.search(r'<gallery[^>]*>(.*?)</gallery>', content, re.DOTALL)
    if gallery:
        print('Gallery content:')
        print(gallery.group(1)[:1500])
