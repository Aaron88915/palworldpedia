#!/usr/bin/env python3
"""Scan every built page in dist/ for broken internal links.

Covers ALL internal hrefs (not just /pals/ and /tech-tree/) so that a new
section like /regions/ or /guides/ cannot ship with dead links.

Exits non-zero when something is broken, so it can gate a commit.
"""
import os
import re
import sys
from urllib.parse import unquote

if not os.path.isdir('dist'):
    print('dist/ not found - run `npm run build` first')
    sys.exit(2)

html_files = []
for root, dirs, files in os.walk('dist'):
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f))

HREF_RE = re.compile(r'href="(/[^"]*)"')

missing = {}
for path in html_files:
    try:
        data = open(path, encoding='utf-8').read()
    except Exception:
        continue
    en_page = path.replace('\\', '/').startswith('dist/en/')
    for m in HREF_RE.finditer(data):
        href = unquote(m.group(1))
        if href.startswith('//') or href.startswith('/_'):
            continue
        target = href.split('#')[0].split('?')[0]
        if not target or target == '/':
            continue
        rel = target.lstrip('/')
        candidates = []
        if target.endswith('/'):
            # Astro emits /404/ as 404.html (special case) and every other
            # route as <route>/index.html
            candidates.append(os.path.join('dist', rel, 'index.html'))
            candidates.append(os.path.join('dist', rel.rstrip('/') + '.html'))
        else:
            candidates.append(os.path.join('dist', rel))
            candidates.append(os.path.join('dist', rel, 'index.html'))
        if not any(os.path.exists(c) for c in candidates):
            missing.setdefault(target, []).append(path)

print('Scanning %d HTML files in dist/ ...' % len(html_files))
print('Distinct broken internal links: %d' % len(missing))
if missing:
    total = sum(len(v) for v in missing.values())
    print('(referenced from %d places)\n' % total)
    for target, paths in sorted(missing.items(), key=lambda kv: -len(kv[1])):
        print('  %-56s x%d' % (target, len(paths)))
        for p in paths[:3]:
            print('      %s' % p.replace('\\', '/').replace('dist/', ''))
    sys.exit(1)

print('OK - no broken internal links')
