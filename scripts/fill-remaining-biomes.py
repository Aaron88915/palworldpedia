#!/usr/bin/env python3
"""Fill the final 7 missing pal biomes.

After variant-copy biome pass and agent fill, 7 pals remained.
Decisions (from paldb.cc / game knowledge):
  - Pengullet Lux:    variant of Pengullet -> Windswept Hills
  - Xenovader:        Feybreak wild Pal
  - Xenogard:         Feybreak wild Pal
  - Bellanoir:        tower boss at Sakurajima Pal Sanctuary
  - Bellanoir Libero: variant of Bellanoir, same location
  - Xenolord:         Feybreak tower boss
  - Hartalis:         Feybreak tower boss
"""
import json
import sys

PATH = 'src/data/pals.json'

# (pal_en_name, biomes)  -- match en name exactly
FIXES = {
    'Pengullet Lux':    ['Windswept Hills'],
    'Xenovader':        ['Feybreak'],
    'Xenogard':         ['Feybreak'],
    'Bellanoir':        ['Sakurajima'],
    'Bellanoir Libero': ['Sakurajima'],
    'Xenolord':         ['Feybreak'],
    'Hartalis':         ['Feybreak'],
}


def main():
    with open(PATH, encoding='utf-8') as f:
        pals = json.load(f)

    fixed = []
    for p in pals:
        en = p['name']['en']
        if en in FIXES and (not p.get('biomes') or len(p['biomes']) == 0):
            p['biomes'] = FIXES[en]
            fixed.append((p['paldeckNo'], en, p['name']['zh'], FIXES[en]))

    if not fixed:
        print('No fixes applied (all already filled).')
        return 0

    with open(PATH, 'w', encoding='utf-8') as f:
        json.dump(pals, f, ensure_ascii=False, indent=2)

    print(f'Fixed {len(fixed)} pals:')
    for paldeckNo, en, zh, biomes in fixed:
        print(f'  #{paldeckNo} {zh} ({en}) -> {biomes}')

    # Verify
    still_missing = [p for p in pals if not p.get('biomes') or len(p['biomes']) == 0]
    print(f'\nStill missing biomes: {len(still_missing)}')
    for p in still_missing:
        print(f'  #{p["paldeckNo"]} {p["name"]["zh"]} ({p["name"]["en"]})')
    return 0


if __name__ == '__main__':
    sys.exit(main())
