import urllib.request
# Test with Referer set to palworldpedia.cc
req = urllib.request.Request('https://cdn.paldb.cc/image/Others/InventoryItemIcon/Texture/T_itemicon_Weapon_Axe_Tier_00.webp', headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://palworldpedia.cc/tech-tree/',
})
r = urllib.request.urlopen(req, timeout=10)
body = r.read()
print(f'With referer: {r.status} {len(body)}B')
print('Headers:')
for k, v in r.headers.items():
    print(f'  {k}: {v}')

# Without referer
req2 = urllib.request.Request('https://cdn.paldb.cc/image/Others/InventoryItemIcon/Texture/T_itemicon_Weapon_Axe_Tier_00.webp', headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
})
r2 = urllib.request.urlopen(req2, timeout=10)
body2 = r2.read()
print(f'\nNo referer: {r2.status} {len(body2)}B')
