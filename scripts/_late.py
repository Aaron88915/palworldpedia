# -*- coding: utf-8 -*-
html = open('scripts/_full_Kingpaca.html', encoding='utf-8').read()
print('Total length:', len(html))
# Show the bottom part of the page (after 75000)
print(html[75000:])
