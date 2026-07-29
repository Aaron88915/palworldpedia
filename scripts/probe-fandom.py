# -*- coding: utf-8 -*-
import urllib.request, json, urllib.parse, time

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json',
}

variants = [
    'Gumoss_Special', 'Ribbuny', 'Wumpo_Botan', 'Faleris',
    'Katress_Ignis', 'Mau_Cryst', 'Mau', 'Vanwyrm_Cryst',
    'Foxparks_Cryst', 'Celaray_Lux', 'Celaray', 'Hoocrates',
    'Lifmunk', 'Lifmunk_Elec',
    'Direhowl', 'Blazamut', 'Suzaku', 'Suzaku_Ignis',
    'Helzephyr', 'Helzephyr_Lux',
    'Faleris', 'Faleris_Blaze',
    'Cawgnito', 'Cawgnito_Dark', 'Nitewing', 'Nitewing_Air',
    'Frostplague', 'Frostplague_Astral',
    'Dazzi_Noct', 'Dazzi', 'Lunaris', 'Noctowl', 'Noctowl_Blaze',
    'Caprity_Noct', 'Caprity',
    'Loupmoon_Cryst', 'Loupmoon',
    'Fenglope_Lux', 'Fenglope',
    'Kitsun_Noct', 'Kitsun', 'Silkcat', 'Silkcat_Obsidian',
    'Celeray', 'Cryolinx_Terra', 'Cryolinx_Hydro',
    'Gumoss', 'Gumoss_Jelly',
    'Wumpo', 'Dumud_Gild', 'Dumud',
    'Petallia', 'Tarantriss', 'Ribbuny', 'Rooby',
    'Fuack', 'Cattiva', 'Pengullet', 'Pengullet_Ignis',
    'Sparkit', 'Pupperai', 'Tanzee', 'Clovee',
    'Hangyu', 'Hangyu_Crusher', 'Jormuntide', 'Jormuntide_Ignis',
    'Quivern', 'Quivern_Blaze', 'Blazamut', 'Blazamut_Royal',
    'Silvegis', 'Silvegis_Alpine', 'Cinnamoth', 'Cinnamoth_Forest',
    'Astegon', 'Astegon_Blaze', 'Smokie', 'Smokie_Dark',
    'Azurobe', 'Azurobe_King', 'Frostallion', 'Frostallion_Ice',
    'Grizzbolt', 'Reptyro', 'Reptyro_Blaze', 'Warsect',
    'Wumpo_Ice', 'Celesphor', 'Celesphor_Emperor',
    'Feybreak', 'Feybreak_Observer',
    'Orserk', 'Orserk_Stream',
    'Bellanoir', 'Bellanoir_Libero',
    'Xandrie', 'Xandrie_Umbral',
    'Prunelia', 'Prunelia_Stone',
    'SilkSpider', 'SilkSpider_Crystal',
    'Splatterina', 'Splatterina_Fantasm',
    'Prixter', 'Prixter_Storm',
    'Yakumo', 'Yakumo_Shadow',
    'Dawn_Master', 'Noctowl_Blaze',
    'Dumud_Blockhead', 'Melpaca', 'Melpaca_Lovely',
]

ok, miss = [], []
for n in variants:
    enc = urllib.parse.quote(n)
    url = f'https://palworld.fandom.com/api.php?action=query&format=json&prop=revisions&titles={enc}&rvprop=content&rvslots=main&redirects=1'
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        r = urllib.request.urlopen(req, timeout=10)
        j = json.loads(r.read().decode('utf-8'))
        pages = j.get('query', {}).get('pages', {})
        redirects = j.get('query', {}).get('redirects', [])
        redirected_to = redirects[0].get('to') if redirects else None
        for pid, p in pages.items():
            if int(pid) > 0:
                revs = p.get('revisions', [])
                if revs:
                    title = p.get('title','')
                    clen = len(revs[0]['slots']['main']['*'])
                    extra = f' (from {redirected_to})' if redirected_to else ''
                    ok.append(f'  {n:30s} -> {title}{extra} [{clen}b]')
                else:
                    miss.append(f'  {n:30s} -> no revision')
            else:
                miss.append(f'  {n:30s} -> MISSING')
    except Exception as e:
        miss.append(f'  {n:30s} -> ERR: {str(e)[:50]}')
    time.sleep(0.1)

print('=== Found ===')
for x in ok: print(x)
print('=== Missing ===')
for x in miss: print(x)
print()
print(f'Summary: {len(ok)} found, {len(miss)} missing')
