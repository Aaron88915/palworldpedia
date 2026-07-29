import urllib.request, json, os, time
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

with open('src/data/tech.json', 'r', encoding='utf-8') as f:
    techs = json.load(f)

OUT = 'public/images/tech'
os.makedirs(OUT, exist_ok=True)

ok, fail, skip = 0, 0, 0
for i, t in enumerate(techs):
    if not t.get('icon'):
        skip += 1
        continue
    url = t['icon']
    # Filename: use the icon's last segment
    fname = url.split('/')[-1]
    out_path = os.path.join(OUT, fname)
    if os.path.exists(out_path) and os.path.getsize(out_path) > 100:
        skip += 1
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
    except Exception as e:
        fail += 1
    if (i + 1) % 30 == 0:
        print(f'[{i+1}/{len(techs)}] ok={ok} fail={fail} skip={skip}')
    time.sleep(0.08)

print(f'\nFinal: ok={ok} fail={fail} skip={skip}')
