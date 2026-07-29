# -*- coding: utf-8 -*-
"""Verify all the previously-missing images are live."""
import urllib.request

names = [
    'Celaray Lux.png', 'Clovee.png', 'Cryolinx Terra.png', 'Dazzi Noct.png',
    'Dumud Gild.png', 'Fenglope Lux.png', 'Foxparks Cryst.png', 'Fuack.png',
    'Green Slime menu.png', 'Gumoss (Special).png', 'Kitsun Noct.png',
    'Loupmoon Cryst.png', 'Panthalus.png', 'Pupperai.png', 'Rooby.png',
    'Sparkit.png', 'Tanzee.png', 'Warsect Terra.png', 'Whalaska Ignis.png',
    'Caprity Noct.png',
]

ok = 0
fail = []
for n in names:
    try:
        r = urllib.request.urlopen(f'https://palworldpedia.cc/images/pals/{urllib.parse.quote(n)}', timeout=10)
        if r.status == 200:
            ok += 1
        else:
            fail.append((n, r.status))
    except Exception as e:
        fail.append((n, str(e)[:50]))

print(f'OK: {ok}/{len(names)}')
if fail:
    print('Failed:')
    for n, e in fail:
        print(f'  {n}: {e}')
