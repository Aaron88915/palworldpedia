# -*- coding: utf-8 -*-
"""Check if work data fix is live."""
import urllib.request, json

# Fetch the live data via the breeding JSON
# Or just verify the work counts by checking the rendered page

# Check via a pal detail page
r = urllib.request.urlopen('https://palworldpedia.cc/pals/grizzbolt/', timeout=15)
d = r.read().decode('utf-8', errors='ignore')
# Check if Grizzbolt now has work icons
has_electricity = '发电' in d or 'generating_electricity' in d
print(f'Grizzbolt page has electricity work: {has_electricity}')

# Better: check the source - look for Orserk which should have generating_electricity
# It's server-rendered, so check the page directly
import re
m = re.search(r'work-grid.*?</section>', d, re.DOTALL)
if m:
    text = re.sub(r'<[^>]+>', ' ', m.group(0))
    text = re.sub(r'\s+', ' ', text).strip()
    print(f'Grizzbolt work section text: {text[:300]}')
