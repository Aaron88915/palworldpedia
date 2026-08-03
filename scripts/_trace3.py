# -*- coding: utf-8 -*-
import sys, importlib.util
spec = importlib.util.spec_from_file_location('fill_biomes', 'scripts/fill-biomes.py')
fb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fb)

# Check all pals in the pals.json that don't have biomes
import json
pals = json.load(open('src/data/pals.json', encoding='utf-8'))
need = [p for p in pals if not p.get('biomes')]
print('Pals without biomes: %d' % len(need))
for p in need:
    pid = p['id']
    paldb_name = fb.slug_to_paldb_name(pid)
    html = fb.fetch_paldb(paldb_name, retries=0)
    biomes = fb.parse_biomes_from_paldb(html)
    print('%-25s -> %s' % (pid, biomes))
