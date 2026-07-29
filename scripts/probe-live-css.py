import urllib.request
req = urllib.request.Request('https://palworldpedia.cc/_astro/index.Bju34icF.css', headers={'User-Agent': 'Mozilla/5.0'})
css = urllib.request.urlopen(req, timeout=30).read().decode('utf-8')
print('LENGTH:', len(css))
# Find .type-fire
import re
for m in re.finditer(r'\.type-(fire|water|grass|electric|ice|ground|dark|dragon|neutral)[^{}]*\{[^}]+\}', css):
    print(m.group(0)[:300])
    print('---')
# Find .chip
for m in re.finditer(r'\.chip[^{}]*\{[^}]+\}', css):
    print(m.group(0)[:300])
    print('---')
