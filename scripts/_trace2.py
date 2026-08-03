# -*- coding: utf-8 -*-
import sys, importlib.util
spec = importlib.util.spec_from_file_location('fill_biomes', 'scripts/fill-biomes.py')
fb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fb)
html = open('scripts/_paldb_cache/Finsider.html', encoding='utf-8', errors='ignore').read()
print('parse Finsider:', fb.parse_biomes_from_paldb(html))

# Also try a few others
for n in ['Flopie', 'Pengullet_Lux', 'Finsider_Ignis', 'Bellanoir', 'Xenolord']:
    path = 'scripts/_paldb_cache/' + n + '.html'
    try:
        html = open(path, encoding='utf-8', errors='ignore').read()
        print('%-20s parse: %s' % (n, fb.parse_biomes_from_paldb(html)))
    except FileNotFoundError:
        print('%-20s NOT FOUND' % n)
