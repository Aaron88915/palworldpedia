#!/usr/bin/env python3
"""把 <AdSlot slot= 全部改成 <AdSlot position= """
import os, re

count = 0
for root, _, files in os.walk('src'):
    for f in files:
        if not f.endswith('.astro'):
            continue
        path = os.path.join(root, f)
        content = open(path, encoding='utf-8').read()
        new_content = content.replace('<AdSlot slot=', '<AdSlot position=')
        if new_content != content:
            n = content.count('<AdSlot slot=')
            count += n
            with open(path, 'w', encoding='utf-8') as out:
                out.write(new_content)
            print(f'{path}: {n} replacements')

print(f'\nTotal: {count} replacements')
