#!/usr/bin/env python3
import re
files = [
    ('src/pages/index.astro', 'src/pages/index.astro'),
    ('src/pages/pals/index.astro', 'src/pages/pals/index.astro'),
    ('src/pages/breeding/index.astro', 'src/pages/breeding/index.astro'),
    ('src/pages/tech-tree/index.astro', 'src/pages/tech-tree/index.astro'),
    ('src/pages/about.astro', 'src/pages/about.astro'),
]
for label, f in files:
    c = open(f, encoding='utf-8').read()
    # 找所有 AdSlot 出现的行号和上下文
    for m in re.finditer(r'<AdSlot', c):
        # find line number
        line_num = c[:m.start()].count('\n') + 1
        line_start = c.rfind('\n', 0, m.start()) + 1
        line_end = c.find('\n', m.end())
        line = c[line_start:line_end if line_end >= 0 else len(c)]
        print(f'{label}:{line_num}: {line.strip()}')
    print()
