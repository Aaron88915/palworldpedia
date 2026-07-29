import urllib.request, re
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
req = urllib.request.Request('https://palworld.wiki.gg/wiki/Breeding', headers=UA)
body = urllib.request.urlopen(req, timeout=20).read().decode('utf-8', errors='ignore')
# Look for technology-related content
for kw in ['Technology', 'Workbench', 'Palbox', 'Material', 'Unlock', 'Craft']:
    idx = body.find(kw)
    if idx > 0:
        ctx = re.sub(r'\s+', ' ', body[max(0,idx-50):idx+200])
        print(f'{kw}: {ctx[:250]}')
        print('---')

# Find all internal wiki links to see what exists
hrefs = re.findall(r'href="(/wiki/[^"]+)"', body)
unique = sorted(set(h for h in hrefs if ':' not in h))
print(f'\nWiki links from Breeding page: {len(unique)}')
# Filter to technology-related
tech_links = [h for h in unique if any(k in h.lower() for k in ['tech', 'craft', 'build', 'palbox', 'work'])]
print('Tech-related:')
for h in tech_links[:20]:
    print(f'  {h}')

# Check if this is MediaWiki (wiki.gg is MediaWiki-based)
print(f'\nGenerator: {re.findall("meta name=.generator. content=.([^\"]+).", body)}')
