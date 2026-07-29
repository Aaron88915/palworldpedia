# -*- coding: utf-8 -*-
"""Extract full text from /breeding-path to understand Path Finder UI."""
import urllib.request, re

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

url = 'https://palworld.gg/breeding-path'
req = urllib.request.Request(url, headers=HEADERS)
data = urllib.request.urlopen(req, timeout=20).read().decode('utf-8', errors='ignore')

# Strip HTML
text = re.sub(r'<script[^>]*>.*?</script>', '', data, flags=re.DOTALL)
text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
text = re.sub(r'<[^>]+>', '\n', text)
text = re.sub(r'\n+', '\n', text)
text = re.sub(r'[ \t]+', ' ', text).strip()

# Print relevant sections
lines = text.split('\n')
in_relevant = False
for i, line in enumerate(lines):
    line = line.strip()
    if not line:
        continue
    if 'Path Finder' in line or 'Shortest' in line or 'You Own' in line or 'chain' in line or 'starting' in line.lower() or 'Select' in line or 'Available' in line or 'result' in line.lower() or 'path' in line.lower() or 'selectable' in line.lower():
        in_relevant = True
    if in_relevant and line:
        print(line[:200])
    if 'Partner Skill' in line and 'Partner' in lines[max(0,i-1)]:
        break
