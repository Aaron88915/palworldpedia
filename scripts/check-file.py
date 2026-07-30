#!/usr/bin/env python3
import os
files = [
    'src/pages/index.astro',
    'src/pages/pals/index.astro',
    'src/pages/breeding/index.astro',
    'src/pages/tech-tree/index.astro',
    'src/pages/about.astro',
    'src/pages/contact.astro',
]
for f in files:
    raw = open(f, 'rb').read()
    bom = 'BOM' if raw.startswith(b'\xef\xbb\xbf') else 'no-BOM'
    has_crlf = 'CRLF' if b'\r\n' in raw else 'LF-only'
    size = len(raw)
    adslot_count = raw.decode('utf-8').count('<AdSlot')
    print(f'{f:<40} {bom:<8} {has_crlf:<8} {size:>7} bytes  {adslot_count} AdSlot')

# Also check if the components dir has a problem
import os
for f in ['src/components/AdSlot.astro']:
    raw = open(f, 'rb').read()
    print(f'\n{f}: {len(raw)} bytes')
    print(raw[:200].decode('utf-8', 'ignore'))
