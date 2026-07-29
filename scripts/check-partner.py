# -*- coding: utf-8 -*-
import json
pals = json.load(open('src/data/pals.json', encoding='utf-8'))

# Check partner for early pals
for p in pals[:10]:
    print(f"{p['id']:25s} partner={p.get('partnerSkill')}")
