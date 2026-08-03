# -*- coding: utf-8 -*-
"""Check spawner regex against actual data."""
import re
html = open('scripts/_paldb_cache/Finsider.html', encoding='utf-8', errors='ignore').read()
# All spawner patterns
for m in re.finditer(r'spawner=[A-Za-z0-9_]+', html):
    print('spawner:', m.group(0))
print()
# All zone= patterns
for m in re.finditer(r'zone=[A-Za-z0-9_]+', html):
    print('zone:', m.group(0))
print()
# Try the new regex
print('--- new regex test ---')
for m in re.finditer(r'spawner=[A-Za-z0-9_]*?(grass|forest|desert|dessert|snow|volcano|dark|sky|moon|feybreak|sakurajima|sanctuary|tropical|island)[A-Za-z0-9_]*', html):
    print('match:', m.group(0), '->', m.group(1))
