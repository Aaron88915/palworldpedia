# -*- coding: utf-8 -*-
import re
for slug in ['gumoss-special', 'cryolinx-terra', 'fuack', 'pupperai', 'clovee', 'foxparks-cryst']:
    with open(f'dist/pals/{slug}/index.html', encoding='utf-8') as f:
        content = f.read()
    print(f'=== {slug} (len={len(content)}) ===')
    h2s = re.findall(r'<h2[^>]*>([^<]+)</h2>', content)
    print(f'  sections: {h2s}')
    # stat values
    for m in re.finditer(r'class="stat-value"[^>]*>([^<]+)</div>', content):
        print(f'  stat: {m.group(1)}')
    # skill names
    skills = re.findall(r'class="skill-name"[^>]*>([^<]+)</span>', content)
    print(f'  skills: {len(skills)} (first 3: {skills[:3]})')
    # drops
    drops = re.findall(r'class="drop-chip"[^>]*>([^<]+)</span>', content)
    print(f'  drops: {drops[:5]}')
    print()
