# -*- coding: utf-8 -*-
"""Fetch the missing paldb.cc pages and see what data is in them."""
import urllib.request, os, re, time, urllib.parse

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

missing_ids = [
    'pengullet-lux', 'kingpaca-cryst', 'mau-cryst', 'foxparks-cryst',
    'fenglope-lux', 'finsider-ignis', 'beakon-cryst', 'needoll-noct',
    'pierdon-cryst', 'whalaska-ignis', 'solmora-lux', 'eidrolon-ignis',
    'bellanoir-libero', 'frostallion-noct',
]

cache_dir = 'scripts/_paldb_cache'
os.makedirs(cache_dir, exist_ok=True)

for pid in missing_ids:
    paldb_name = ' '.join(s.capitalize() for s in pid.split('-'))
    cache_path = os.path.join(cache_dir, paldb_name.replace(' ', '_') + '.html')
    url = 'https://paldb.cc/en/' + urllib.parse.quote(paldb_name)
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        r = urllib.request.urlopen(req, timeout=20)
        html = r.read().decode('utf-8', errors='ignore')
        open(cache_path, 'w', encoding='utf-8', errors='ignore').write(html)
        # Quick check for spawner / zone data
        spawners = re.findall(r'spawner=([A-Za-z0-9_]+)', html)
        zones = re.findall(r'zone=([a-z_]+)_grade_\d+', html)
        recruiters = re.findall(r'Pal Recruiter:\s*([A-Za-z_]+)', html)
        print('%-25s OK %d bytes | spawners=%d zones=%d recruiters=%d' % (pid, len(html), len(spawners), len(zones), len(recruiters)))
        if recruiters:
            print('  -> Pal Recruiter: %s' % recruiters)
        if spawners[:3]:
            print('  -> spawners: %s' % spawners[:3])
        if zones[:3]:
            print('  -> zones: %s' % zones[:3])
    except Exception as e:
        print('%-25s ERR %s' % (pid, e))
    time.sleep(0.3)
