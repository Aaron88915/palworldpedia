import urllib.request, re, socket, json, time, os
socket.setdefaulttimeout(60)
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

OUT = 'scripts/paldb-tech-html'
os.makedirs(OUT, exist_ok=True)

with open('scripts/raw-tech-list.json', 'r', encoding='utf-8') as f:
    techs = json.load(f)

print(f'Total techs to fetch: {len(techs)}')

ok, fail, skip = 0, 0, 0
for i, t in enumerate(techs):
    slug = t['slug']
    outfile = os.path.join(OUT, f'{slug}.html')
    if os.path.exists(outfile) and os.path.getsize(outfile) > 1000:
        skip += 1
        continue
    url = f'https://paldb.cc/en/{slug}'
    try:
        req = urllib.request.Request(url, headers=UA)
        r = urllib.request.urlopen(req, timeout=20)
        body = r.read().decode('utf-8')
        with open(outfile, 'w', encoding='utf-8') as f:
            f.write(body)
        ok += 1
    except urllib.error.HTTPError as e:
        if e.code == 404:
            # Save empty marker
            with open(outfile, 'w', encoding='utf-8') as f:
                f.write('')
            fail += 1
        else:
            fail += 1
    except Exception as e:
        fail += 1

    if (i + 1) % 20 == 0:
        print(f'[{i+1}/{len(techs)}] ok={ok} fail={fail} skip={skip}')
    time.sleep(0.15)

print(f'\nFinal: ok={ok} fail={fail} skip={skip}')
