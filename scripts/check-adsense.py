with open('dist/index.html', 'r', encoding='utf-8') as f:
    html = f.read()
print('adsbygoogle.js script:', 'pagead/js/adsbygoogle' in html)
print('ins tag count:', html.count('class="adsbygoogle"'))
print('client ID present:', 'ca-pub-6473783239192829' in html)
