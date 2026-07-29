# -*- coding: utf-8 -*-
"""Compare breeding page UI details."""
import urllib.request, re

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

req = urllib.request.Request('https://palworld.gg/breeding-calculator', headers=HEADERS)
r = urllib.request.urlopen(req, timeout=15)
data = r.read().decode('utf-8', errors='ignore')

# Strip HTML for clean text
text = re.sub(r'<script[^>]*>.*?</script>', '', data, flags=re.DOTALL)
text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
text = re.sub(r'<[^>]+>', ' ', text)
text = re.sub(r'\s+', ' ', text).strip()

# Find sections with breeding info
for kw in ['breed', 'combine', 'offspring', 'chain', 'shortest', 'gender', 'male', 'female', 'parent', 'child']:
    idx = text.lower().find(kw)
    if idx > 0:
        print(f'  [{kw}@{idx}]: {text[max(0,idx-30):idx+150]}')

# Count mentions
import re
counts = {}
for kw in ['Gender', 'Male', 'Female', 'Child', 'Parent', 'Breed', 'Combos', 'Shortest', 'Forward', 'Reverse']:
    counts[kw] = text.count(kw)
print('\nKeyword counts:')
for k, v in counts.items():
    print(f'  {k}: {v}')

# Find form/select structure
forms = re.findall(r'<form[^>]*>(.*?)</form>', data, re.DOTALL)
print(f'\nForms: {len(forms)}')

# Look for gender indicators (we don't have these!)
gender_pat = re.findall(r'(gender|♂|♀)', text, re.IGNORECASE)
print(f'Gender references: {len(gender_pat)}')
