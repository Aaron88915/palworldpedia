import json, os, urllib.request, time
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

# Direct URL mapping for the 8 still missing
fills = {
    'Antique Dresser': 'T_icon_buildObject_TableDresser01_Stone.png',
    'Summoning Altar': 'T_icon_buildObject_Altar.png',
    'Electric Egg Incubator': 'T_icon_buildObject_ElectricHatchingPalEgg.png',
    'Large Incubator': 'T_icon_buildObject_MultiHatchingPalEgg.png',
    'Large Power Generator': 'T_icon_buildObject_ElectricGenerator_Large.png',
    'Large-Scale Electric Egg Incubator': 'T_icon_buildObject_MultiElectricHatchingPalEgg.png',
    'Ancient Hatchery': 'T_icon_buildObject_MultiElectricHatchingPalEggWithBreed.png',
    'Wing Pack': 'T_itemicon_Glider_WingGlider.png',
}

OUT = 'public/images/tech'
os.makedirs(OUT, exist_ok=True)

with open('src/data/tech.json', 'r', encoding='utf-8') as f:
    techs = json.load(f)

ok, fail = 0, 0
for t in techs:
    if t['name'] not in fills:
        continue
    if not t['icon'].startswith('https://cdn.paldb.cc/'):
        continue
    fname = fills[t['name']]
    out_path = os.path.join(OUT, fname)
    if not (os.path.exists(out_path) and os.path.getsize(out_path) > 100):
        url = f'https://palworld.gg/images/items/{fname}'
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
            print(f'  FAIL {t["name"]}: {e}')
            fail += 1
            continue
    t['icon'] = '/images/tech/' + fname
    ok += 1

# Save
with open('src/data/tech.json', 'w', encoding='utf-8') as f:
    json.dump(techs, f, ensure_ascii=False, indent=1)

# Check
still_cdn = [t for t in techs if t['icon'].startswith('https://cdn.paldb.cc/')]
print(f'Filled {ok}, failed {fail}')
print(f'Still CDN: {len(still_cdn)}')
for t in still_cdn:
    print(f'  {t["name"]}')
