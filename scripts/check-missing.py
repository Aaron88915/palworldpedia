import json
with open('src/data/tech.json', 'r', encoding='utf-8') as f:
    techs = json.load(f)
our_names = {t['name'] for t in techs}

# Sample of 19 we found in paldb.cc but with different names
# Let's check what our data has for similar items
print('=== Our data has these (look for matches) ===')
for kw in ['Spear', 'Harness', 'Saddle', 'Workbench', 'Crusher', 'Wall', 'Gatling', 'Shotgun', 'Missile', 'Cart', 'Hammer', 'Bow', 'Rifle']:
    matches = [t['name'] for t in techs if kw in t['name']]
    if matches:
        print(f'  {kw}: {matches[:5]}')

# So the issue is: paldb.cc list has these 19 but our data has them under similar names
# E.g. 'Lily Spear' (no apostrophe) vs 'Lily's Spear' (with apostrophe)
# Let me check specific ones
print()
print('=== Check specific 19 ===')
suspects = [
    ("Lily's Spear", 'Lily Spear'),
    ("Foxparks' Harness", 'Foxparks Harness'),
    ("Jetragon's Missile Launcher", 'Jetragon Missile Launcher'),
    ("Bastigor's Hammer", 'Bastigor Hammer'),
    ("Direhowl's Saddled Harness", 'Direhowl Saddled Harness'),
    ("Stone Defensive Wall", 'Defensive Wall'),
]
for target, alt in suspects:
    in_ours = any(t['name'] == target for t in techs)
    alt_in_ours = any(t['name'] == alt for t in techs)
    print(f'  {target!r}: in_ours={in_ours}, alt={alt!r} alt_in_ours={alt_in_ours}')

# Check cost for an interesting one - High Quality Workbench
hq_workbench = [t for t in techs if 'workbench' in t['name'].lower() and ('quality' in t['name'].lower() or 'high' in t['name'].lower())]
print(f'\nHigh/Quality Workbench: {hq_workbench}')

# Mining Cart
cart = [t for t in techs if 'cart' in t['name'].lower()]
print(f'Cart: {cart}')

# Defensive Wall
walls = [t for t in techs if 'wall' in t['name'].lower() and 'defensive' in t['name'].lower()]
print(f'Defensive Wall: {walls}')

# Refrigerated Crusher
crushers = [t for t in techs if 'crusher' in t['name'].lower()]
print(f'Crusher: {crushers}')
