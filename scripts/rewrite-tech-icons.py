import json, os

with open('src/data/tech.json', 'r', encoding='utf-8') as f:
    techs = json.load(f)

# Map cdn URL -> local path
LOCAL_DIR = 'public/images/tech'
if not os.path.isdir(LOCAL_DIR):
    os.makedirs(LOCAL_DIR, exist_ok=True)

mapped, missing = 0, 0
for t in techs:
    if not t.get('icon'):
        continue
    url = t['icon']
    fname = url.split('/')[-1]
    local = f'/images/tech/{fname}'
    local_disk = os.path.join(LOCAL_DIR, fname)
    if os.path.exists(local_disk) and os.path.getsize(local_disk) > 100:
        t['icon'] = local
        mapped += 1
    else:
        # Keep cdn URL as fallback
        missing += 1

with open('src/data/tech.json', 'w', encoding='utf-8') as f:
    json.dump(techs, f, ensure_ascii=False, indent=1)
print(f'Mapped {mapped} to local, {missing} still CDN (download pending)')
