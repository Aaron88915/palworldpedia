# -*- coding: utf-8 -*-
"""Check rarity for known legendaries to set tier thresholds."""
import urllib.request, re, time

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

# Slug overrides
SLUGS = {
    'Jetragon': 'Jetragon',
    'Frostallion': 'Frostallion',
    'Frostallion Noct': 'Frostallion_Noct',
    'Paladius': 'Paladius',
    'Necromus': 'Necromus',
    'Neptilius': 'Neptilius',
    'Panthalus': 'Panthalus',
    # Edge cases
    'Lamball': 'Lamball',
    'Cattiva': 'Cattiva',
    'Lifmunk': 'Lifmunk',
    'Celaray Lux': 'Celaray_Lux',
    'Kitsun Noct': 'Kitsun_Noct',
    'Jormuntide': 'Jormuntide',
    'Jormuntide Ignis': 'Jormuntide_Ignis',
    'Cryolinx Terra': 'Cryolinx_Terra',
    'Blazamut': 'Blazamut',
    'Blazamut Ryu': 'Blazamut_Ryu',
    'Bellanoir': 'Bellanoir',
    'Bellanoir Libero': 'Bellanoir_Libero',
    'Gumoss (Special)': 'Gumoss_(Special)',
    'Rayhound': 'Rayhound',
    'Anubis': 'Anubis',
    'Astegon': 'Astegon',
    'Orserk': 'Orserk',
    'Shadowbeak': 'Shadowbeak',
    'Silvegis': 'Silvegis',
    'Xenolord': 'Xenolord',
    'Warsect': 'Warsect',
    'Suzaku': 'Suzaku',
    'Ice King': 'Ice_King',  # Frostallion variant?
    'Helzephyr': 'Helzephyr',
    'Silvegis Noct': 'Silvegis_Noct',
    'Silvegis Lux': 'Silvegis_Lux',
}

def get_rarity(slug):
    url = f'https://paldb.cc/en/{slug}'
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        r = urllib.request.urlopen(req, timeout=15)
        d = r.read().decode('utf-8', errors='ignore')
        m = re.search(r'<div>Rarity</div>.*?<div>(\d+)</div>', d, re.DOTALL)
        if m:
            return int(m.group(1))
    except Exception as e:
        return f'ERR {e}'
    return None

for en, slug in SLUGS.items():
    n = get_rarity(slug)
    print(f'  {en:25s} -> {n}')
    time.sleep(0.3)
