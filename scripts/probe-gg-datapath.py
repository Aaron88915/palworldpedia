# -*- coding: utf-8 -*-
"""Find actual data path from bundle."""
import re

with open('scripts/palworldgg-bundles/CpWWtyX8.js', encoding='utf-8') as f:
    d = f.read()
# Find the data path
for m in re.finditer(r'["\']([^"\']*data/pals/[^"\']+)["\']', d):
    print(m.group(1))
