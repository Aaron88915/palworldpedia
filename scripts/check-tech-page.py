import re
with open('dist/tech-tree/index.html', 'r', encoding='utf-8') as f:
    html = f.read()
# Match all image src
all_imgs = re.findall(r'<img src="([^"]+)"', html)
print(f'Total imgs: {len(all_imgs)}')
# Group by type
tech_imgs = [i for i in all_imgs if 'palworldpedia' in i or 'paldb' in i]
print(f'Tech imgs: {len(tech_imgs)}')
# Check empty/missing
empty = re.findall(r'<img src=""', html)
print(f'Empty src: {len(empty)}')
non_cdn = [i for i in all_imgs if 'paldb' not in i and 'palworldpedia' not in i]
print(f'Non-CDN: {len(non_cdn)}')
if non_cdn:
    print('First few:', non_cdn[:3])
