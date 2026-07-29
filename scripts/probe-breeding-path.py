# -*- coding: utf-8 -*-
"""Probe /breeding-path page on palworld.gg to understand Path Finder."""
import urllib.request, re, json

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

# Try the Path Finder page
for url in ['https://palworld.gg/breeding-path', 'https://palworld.gg/breeding-calculator']:
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        r = urllib.request.urlopen(req, timeout=20)
        data = r.read().decode('utf-8', errors='ignore')
        print(f'\n========== {url} (status={r.status}, len={len(data)}) ==========')

        # Strip HTML for text analysis
        text = re.sub(r'<script[^>]*>.*?</script>', '', data, flags=re.DOTALL)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()

        # Find sections of interest
        markers = ['Path Finder', 'Shortest', 'You Own', 'selectable', 'pal world', 'starting', 'path', 'chain', 'Available Pals', 'Select Pals You Own', 'how to breed']
        for m in markers:
            idx = text.find(m)
            if idx > 0:
                print(f'\n--- "{m}" @ {idx} ---')
                print(text[max(0,idx-150):idx+500])
                print('...')
                break

        # Look for inline JSON data
        scripts = re.findall(r'<script[^>]*>(.*?)</script>', data, re.DOTALL)
        for i, s in enumerate(scripts):
            if len(s) > 1000 and 'pals' in s.lower():
                print(f'\n--- Inline script {i} (len={len(s)}): first 800 chars ---')
                print(s[:800])

    except Exception as e:
        print(f'{url}: ERR {e}')
