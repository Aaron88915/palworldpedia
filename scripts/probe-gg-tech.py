import urllib.request, re, json, socket
socket.setdefaulttimeout(60)
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

# Try palworld.gg technology tree page
url = 'https://palworld.gg/technology-tree'
try:
    req = urllib.request.Request(url, headers=UA)
    r = urllib.request.urlopen(req, timeout=30)
    body = r.read().decode('utf-8')
    print(f'OK {r.status} {len(body)} bytes')
    with open('scripts/gg-techtree.html', 'w', encoding='utf-8') as f:
        f.write(body)
except Exception as e:
    print(f'FAIL: {e}')

# Check what's in it
with open('scripts/gg-techtree.html', 'r', encoding='utf-8') as f:
    html = f.read()
# Find image URLs
imgs = re.findall(r'<img[^>]+src="([^"]+)"', html)
print(f'Total imgs: {len(imgs)}')
# Look for our missing tech names
missing_names = ['Palbox', 'Pal Sphere', 'Global Palbox', 'Normal Parachute', 'Bear Trap',
                 'Faux Greenery Set', 'Tidy Table Set', 'Wooden Board', 'Mega Glider',
                 'Bathroom Set', 'Stone Structure Set', 'Tomato Plantation']
for name in missing_names:
    idx = html.find(name)
    if idx > 0:
        ctx = re.sub(r'\s+', ' ', html[max(0,idx-300):idx+200])
        print(f'\n{name}: {ctx[:400]}')
    else:
        print(f'\n{name}: NOT FOUND')

# Find json/nuxt data
print()
print('=== Looking for nuxt data ===')
for m in re.finditer(r'__NUXT__|window\.__|nuxtData', html):
    idx = m.start()
    ctx = re.sub(r'\s+', ' ', html[idx:idx+300])
    print(f'@{idx}: {ctx[:200]}')
    break
