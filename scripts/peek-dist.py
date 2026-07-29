# -*- coding: utf-8 -*-
import re

# Look at gumoss-special and cryolinx-terra in detail
for path in ['dist/pals/gumoss-special/index.html', 'dist/pals/cryolinx-terra/index.html']:
    with open(path, encoding='utf-8') as f:
        content = f.read()
    print(f'=== {path} ===')

    # Find stat-grid
    m = re.search(r'<div class="stat-grid">(.*?)</div>\s*</section>', content, re.DOTALL)
    if m:
        print('  stat-grid HTML:')
        print('  ' + m.group(1)[:2000].replace('\n', ' '))
    print()
