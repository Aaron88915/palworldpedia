# -*- coding: utf-8 -*-
import urllib.request, re

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

req = urllib.request.Request('https://paldb.cc/en/Lamball', headers=HEADERS)
r = urllib.request.urlopen(req, timeout=15)
data = r.read().decode('utf-8', errors='ignore')

# Find all sections that contain "Wild" with lamball info
# Show structure
idx = data.find('Wild')
print(f'Wild first at: {idx}')

# Find "Wild" in heading
for m in re.finditer(r'<h([1-6])[^>]*>([^<]*Wild[^<]*)</h\1>', data, re.IGNORECASE):
    heading = m.group(2)
    start = m.end()
    # Find next h tag
    next_h = re.search(r'<h[1-6][^>]*>', data[start:])
    end = start + next_h.start() if next_h else start + 5000
    chunk = data[start:end]
    text = re.sub(r'<[^>]+>', ' ', chunk)
    text = re.sub(r'\s+', ' ', text).strip()
    print(f'\n=== H{m.group(1)} "{heading}" ===')
    print(text[:2000])
    print('...')

# Also find "Dawn" / "Night" / "Nocturnal" / "Time"
for kw in ['Nocturnal', 'Time of Day', 'Day/Night', 'Spawn Time', 'Breeding']:
    idx = data.find(kw)
    if idx > 0:
        print(f'\n=== {kw} at {idx} ===')
        chunk = data[idx:idx+500]
        text = re.sub(r'<[^>]+>', ' ', chunk)
        text = re.sub(r'\s+', ' ', text).strip()
        print(text[:400])
