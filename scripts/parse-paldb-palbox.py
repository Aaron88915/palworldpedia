import urllib.request, re, socket
socket.setdefaulttimeout(60)
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

# Try different URL patterns for tech detail pages
test_slugs = ['Workbench', 'Palbox', 'Stone_Axe', 'Campfire', 'HandTorch', 'PALBOX', 'Wooden_Chest']
for slug in test_slugs:
    for url_pattern in [f'https://paldb.cc/en/{slug}', f'https://paldb.cc/en/T_{slug}']:
        try:
            req = urllib.request.Request(url_pattern, headers=UA)
            r = urllib.request.urlopen(req, timeout=20)
            body = r.read().decode('utf-8')
            # Quick check if page has tech-specific content
            if slug.lower().replace('_', ' ') in body.lower():
                # Find first occurrence
                idx = body.lower().find(slug.lower().replace('_', ' '))
                ctx = re.sub(r'\s+', ' ', body[max(0,idx-30):idx+200])
                print(f'OK {url_pattern}: {r.status} - {ctx[:200]}')
            else:
                print(f'OK but no match {url_pattern}: {r.status}')
        except Exception as e:
            print(f'FAIL {url_pattern}: {type(e).__name__}: {e}')
