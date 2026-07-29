import urllib.request, json, os, time
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

with open('scripts/gg-tech-icon-map.json', 'r', encoding='utf-8') as f:
    gg_map = json.load(f)

with open('src/data/tech.json', 'r', encoding='utf-8') as f:
    techs = json.load(f)

OUT = 'public/images/tech'
os.makedirs(OUT, exist_ok=True)

# Test a single direct URL
test_url = 'https://palworld.gg/images/items/T_icon_buildObject_PalBoxV2.png'
try:
    req = urllib.request.Request(test_url, headers=UA)
    r = urllib.request.urlopen(req, timeout=10)
    body = r.read()
    print(f'Test direct URL: {r.status} {len(body)}B')
except Exception as e:
    print(f'Test direct URL FAIL: {e}')
    # Try the _ipx one
    test_url = 'https://palworld.gg/_ipx/q_80&s_100x100/images/items/T_icon_buildObject_PalBoxV2.png'
    try:
        req = urllib.request.Request(test_url, headers=UA)
        r = urllib.request.urlopen(req, timeout=10)
        body = r.read()
        print(f'Test ipx URL: {r.status} {len(body)}B')
    except Exception as e2:
        print(f'Test ipx URL FAIL: {e2}')

# Find missing techs in our data
missing = [t for t in techs if t['icon'].startswith('https://cdn.paldb.cc/')]
print(f'\nMissing: {len(missing)}')

ok, fail = 0, 0
for t in missing:
    if t['name'] not in gg_map:
        fail += 1
        continue
    direct = gg_map[t['name']]['direct']  # e.g. /images/items/...
    url = 'https://palworld.gg' + direct
    fname = direct.split('/')[-1]
    out_path = os.path.join(OUT, fname)
    if os.path.exists(out_path) and os.path.getsize(out_path) > 100:
        ok += 1
        t['icon'] = '/images/tech/' + fname  # update to local
        continue
    try:
        req = urllib.request.Request(url, headers=UA)
        r = urllib.request.urlopen(req, timeout=15)
        body = r.read()
        if len(body) < 100:
            fail += 1
            continue
        with open(out_path, 'wb') as f:
            f.write(body)
        ok += 1
        t['icon'] = '/images/tech/' + fname
    except Exception as e:
        fail += 1
    time.sleep(0.05)

print(f'Downloaded: {ok}, failed: {fail}')

# Save updated tech.json
with open('src/data/tech.json', 'w', encoding='utf-8') as f:
    json.dump(techs, f, ensure_ascii=False, indent=1)
print('tech.json updated')

# Check remaining
still_cdn = [t for t in techs if t['icon'].startswith('https://cdn.paldb.cc/')]
print(f'Still CDN: {len(still_cdn)}')
for t in still_cdn:
    print(f'  {t["name"]}')
