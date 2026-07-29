import urllib.request, re, socket
socket.setdefaulttimeout(60)
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

req = urllib.request.Request('https://paldb.cc/en/Palbox', headers=UA)
html = urllib.request.urlopen(req, timeout=60).read().decode('utf-8')

with open('scripts/paldb-palbox.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f'Saved {len(html)} bytes')
