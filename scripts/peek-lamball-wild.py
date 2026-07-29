# -*- coding: utf-8 -*-
import urllib.request, json, urllib.parse, re

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36', 'Accept': 'application/json'}

# Lamball full content
url = f'https://palworld.fandom.com/api.php?action=query&format=json&prop=revisions&titles=Lamball&rvprop=content&rvslots=main'
req = urllib.request.Request(url, headers=HEADERS)
j = json.loads(urllib.request.urlopen(req, timeout=15).read().decode('utf-8'))
pages = j.get('query',{}).get('pages',{})
for pid, p in pages.items():
    content = p['revisions'][0]['slots']['main']['*']
    # Find Wild Spawn section
    m = re.search(r'===\s*Wild Spawn\s*===(.*?)(?====|\Z)', content, re.DOTALL)
    if m:
        print('=== Wild Spawn section ===')
        print(m.group(1)[:1500])
    else:
        print('NO Wild Spawn section found')
        # Show all section headers
        sections = re.findall(r'^=+\s*([^=]+?)\s*=+\s*$', content, re.MULTILINE)
        print('All sections:')
        for s in sections:
            print(' ', s)
