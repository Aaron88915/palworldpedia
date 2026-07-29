# -*- coding: utf-8 -*-
import urllib.request, re

req = urllib.request.Request('https://palworld.gg/', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'})
try:
    r = urllib.request.urlopen(req, timeout=15)
    data = r.read().decode('utf-8', errors='ignore')
    print(f'Status: {r.status}, len: {len(data)}')
    title = re.search(r'<title>([^<]+)</title>', data)
    if title:
        print(f'Title: {title.group(1)}')
    # Find main headers
    headers = re.findall(r'<h([1-3])[^>]*>([^<]+)</h\1>', data)
    print('Top headers:')
    for h in headers[:20]:
        print(f'  h{h[0]}: {h[1].strip()[:80]}')
    # Look for nav links
    nav_links = re.findall(r'<a[^>]+href="(/[^"]+)"[^>]*>([^<]+)</a>', data)
    print('Nav links (first 15):')
    for href, text in nav_links[:15]:
        print(f'  {href} -> {text.strip()[:50]}')
    # Find sections
    sections = re.findall(r'<section[^>]*class="([^"]+)"', data)
    print(f'Section classes: {set(sections)}')
    # Find any data tables or major divs
    main_divs = re.findall(r'<main[^>]*>(.*?)</main>', data, re.DOTALL)
    if main_divs:
        print(f'Main content length: {len(main_divs[0])}')
    # Find footer links
    footer = re.findall(r'<footer[^>]*>(.*?)</footer>', data, re.DOTALL)
    if footer:
        footer_text = re.sub(r'<[^>]+>', ' ', footer[0])
        print(f'Footer: {footer_text[:300]}')
except Exception as e:
    print(f'ERR: {e}')
