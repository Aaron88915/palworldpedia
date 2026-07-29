import urllib.request, re
UA = {'User-Agent': 'Mozilla/5.0'}
req = urllib.request.Request('https://palworld.wiki.gg/', headers=UA)
body = urllib.request.urlopen(req, timeout=20).read().decode('utf-8', errors='ignore')
# Find all wiki/* links
hrefs = re.findall(r'href="(/wiki/[^"]+)"', body)
unique = sorted(set(hrefs))
print(f'Wiki links: {len(unique)}')
for h in unique:
    print(f'  {h}')
