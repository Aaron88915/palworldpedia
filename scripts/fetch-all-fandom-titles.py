# -*- coding: utf-8 -*-
"""Fetch all Fandom wiki page titles via pagination."""
import urllib.request, json, urllib.parse, time, sys

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json',
}

all_titles = []
apcontinue = None
pages = 0

while True:
    url = 'https://palworld.fandom.com/api.php?action=query&format=json&list=allpages&aplimit=500&apnamespace=0'
    if apcontinue:
        url += '&apcontinue=' + urllib.parse.quote(apcontinue)
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        r = urllib.request.urlopen(req, timeout=30)
        j = json.loads(r.read().decode('utf-8'))
    except Exception as e:
        print(f'ERR: {e}')
        time.sleep(2)
        continue

    batch = j.get('query', {}).get('allpages', [])
    titles = [p.get('title') for p in batch]
    all_titles.extend(titles)
    pages += 1

    apcontinue = j.get('continue', {}).get('apcontinue')
    print(f'Page {pages}: got {len(titles)} titles, total {len(all_titles)}', flush=True)
    if not apcontinue:
        break
    time.sleep(0.3)

print(f'\nTotal titles: {len(all_titles)}')
json.dump(all_titles, open('scripts/fandom-all-titles.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('Saved to scripts/fandom-all-titles.json')

# Quick stats
pal_like = [t for t in all_titles if ' ' in t and not any(x in t for x in ['Category:', 'Template:', 'File:', 'User:', 'Help:', 'Palpedia/', 'Update', 'List of', 'How to', 'Guide', 'Patch Notes', 'Server', 'Item', 'Skill', 'Weapon', 'Armor', 'Sphere', 'Medicine', 'Potion', 'Food', 'Seed', 'Material', 'Ore', 'Ingot', 'Arrow', 'Bullet', 'Gloves', 'Helmet', 'Accessory', 'Ring', 'Shield', 'Cape', 'Bow', 'Gun', 'Rifle', 'Shotgun', 'Launcher', 'Club', 'Spear', 'Sword', 'Knife', 'Hammer', 'Axe', 'Pickaxe', 'Sickle', 'Incubator', 'Crusher', 'Refrigerator', 'Stove', 'Pot', 'Table', 'Bed', 'Box', 'Chest', 'Locker', 'Statue', 'Sign', 'Spa', 'Lamp', 'Light', 'Chair', 'Sofa', 'Rug', 'Curtain', 'Desk', 'Book', 'Note', 'Crate', 'Cutter', 'Bag', 'Pillow', 'Pond', 'Ladder', 'Door', 'Wall', 'Floor', 'Stair', 'Ramp', 'Bridge', 'Dye', 'Paint', 'Glue', 'Wire', 'Circuit', 'Battery', 'Pallet', 'Sphere', 'Fruit', 'Berry', 'Mushroom', 'Mutton', 'Wool', 'Cotton', 'Leather', 'Bone', 'Claw', 'Horn', 'Liquid', 'Oil', 'Venom', 'Gland', 'Heart', 'Scale', 'Feather', 'Cloth', 'Fiber', 'Flour', 'Sugar', 'Salt', 'Spice', 'Cake', 'Pie', 'Bread', 'Soup', 'Stew', 'Salad', 'Sushi', 'Sandwich', 'Pancake', 'Jam', 'Honey', 'Milk', 'Egg', 'Drop', 'Shard', 'Crystal', 'Coal', 'Stone', 'Sand', 'Clay', 'Soil', 'Dung', 'Pellet', 'Powder', 'Pellets', 'Tonic', 'Capsule', 'Remedy', 'Extract', 'Essence', 'Meat', 'Jerk', 'Sausage', 'Roast', 'Lettuce', 'Tomato', 'Wheat', 'Corn', 'Carrot', 'Onion', 'Potato', 'Garlic', 'Chili', 'Rice', 'Noodle', 'Pasta', 'Cheese', 'Butter', 'Cream', 'Yogurt', 'Bean', 'Nut', 'Almond', 'Walnut', 'Chestnut', 'Acorn', 'Gum', 'Resin', 'Sap', 'Tar', 'Goo', 'Slime', 'Jelly', 'Pearl', 'Coral', 'Shell', 'Fish', 'Meat', 'Dinosaur', 'Meteor', 'Comet', 'Fragment', 'Part', 'Piece', 'Module', 'Unit', 'Core', 'Circuit', 'Computer', 'Screen', 'Camera', 'Sensor', 'Antenna', 'Battery', 'Cable', 'Wire', 'Switch', 'Panel', 'Key', 'Lock', 'Keycard', 'Token', 'Coin', 'Medal', 'Badge', 'Banner', 'Flag', 'Crown', 'Trophy', 'Gift', 'Box', 'Pack', 'Bundle', 'Bag', 'Sack', 'Pouch', 'Box', 'Chest', 'Locker', 'Crate', 'Bin', 'Trash', 'Recycle', 'Compost', 'Garbage', 'Waste', 'Ashes', 'Soot', 'Charcoal', 'Coke', 'Plastic', 'Rubber', 'Glass', 'Metal', 'Steel', 'Aluminum', 'Copper', 'Iron', 'Gold', 'Silver', 'Platinum', 'Titanium', 'Quartz', 'Marble', 'Granite', 'Slate', 'Sandstone', 'Limestone', 'Obsidian', 'Volcanic', 'Magma', 'Lava', 'Fire', 'Ice', 'Water', 'Electric', 'Grass', 'Ground', 'Dark', 'Dragon', 'Normal', 'Neutral', 'Type', 'Element', 'Type Chart', 'Technology', 'Build', 'Structure', 'Defense', 'Trap', 'Alarm', 'Cage', 'Incubator', 'Breeding', 'Hatching', 'Patch', 'Note', 'Tip', 'Trivia', 'Tactics', 'Mechanics', 'Tutorial', 'Reference', 'Style', 'Logo', 'Banner', 'Icon', 'Image', 'Gallery', 'Wallpaper', 'Artwork', 'Concept', 'Lore', 'Story', 'History', 'Version', 'Beta', 'Alpha', 'Demo', 'Update', 'Roadmap', 'FAQ', 'Q&A', 'Discussion', 'Forum', 'Chat', 'Discord', 'Twitter', 'Facebook', 'Instagram', 'YouTube', 'Twitch', 'Steam', 'Xbox', 'PlayStation', 'Switch', 'PC', 'Mobile', 'App', 'Game', 'Mod', 'Cheat', 'Bug', 'Issue', 'Error', 'Crash', 'Performance', 'Optimization', 'Settings', 'Options', 'Configuration', 'Save', 'Load', 'Backup', 'Restore', 'Import', 'Export', 'Sync', 'Multiplayer', 'Co-op', 'PvP', 'Server', 'Admin', 'Mod', 'Role', 'Permission', 'Ban', 'Kick', 'Mute', 'Whisper', 'Chat', 'Message', 'Mail', 'Inbox', 'Outbox', 'Sent', 'Draft', 'Archive', 'Trash', 'Spam', 'Junk', 'Filter', 'Block', 'Report', 'Appeal', 'Warning', 'Strike', 'Suspend', 'Ban', 'Forum', 'Topic', 'Thread', 'Post', 'Comment', 'Reply', 'Edit', 'Create', 'Delete', 'Move', 'Merge', 'Split', 'Redirect', 'Stub', 'Disambig', 'Template', 'Category', 'Help', 'Project', 'Manual', 'Style Guide', 'Policy', 'Rules', 'Admin', 'User', 'User talk', 'User blog', 'User profile', 'Forum', 'Special', 'Media', 'File', 'Image', 'Video', 'Audio', 'Document', 'PDF', 'Archive', 'Log', 'Statistics', 'Popular', 'Random', 'Recent', 'Changes'])]
print(f'Pal-like titles (filtered): {len(pal_like)}')
for t in pal_like[:30]:
    print(' ', t)
