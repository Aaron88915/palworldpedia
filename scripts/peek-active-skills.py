# -*- coding: utf-8 -*-
import urllib.request, json, urllib.parse, re

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36', 'Accept': 'application/json'}

# Check Lamball (has full skills)
url = f'https://palworld.fandom.com/api.php?action=query&format=json&prop=revisions&titles=Lamball&rvprop=content&rvslots=main'
j = json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=15).read().decode('utf-8'))
content = list(j['query']['pages'].values())[0]['revisions'][0]['slots']['main']['*']

# Find Active Skills section
m = re.search(r'==\s*Active Skills\s*==(.*?)(?====|\Z)', content, re.DOTALL)
if m:
    print('=== Active Skills section (first 3000 chars) ===')
    print(m.group(1)[:3000])
