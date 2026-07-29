# -*- coding: utf-8 -*-
import urllib.request, re
r = urllib.request.urlopen('https://palworldpedia.cc/pals/', timeout=15)
d = r.read().decode('utf-8', errors='ignore')
m = re.findall(r'data-filter-value="([^"]+)" data-filter-group="work"', d)
print('Work filter IDs in HTML:', sorted(set(m)))
