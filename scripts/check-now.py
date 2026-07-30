#!/usr/bin/env python3
import urllib.request, json, re
print('=== GitHub Actions ===')
try:
    req = urllib.request.Request('https://api.github.com/repos/Aaron88915/palworldpedia/actions/runs?per_page=3', headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/vnd.github+json'})
    data = json.loads(urllib.request.urlopen(req, timeout=15).read().decode('utf-8'))
    for run in data.get('workflow_runs', []):
        sha = run['head_sha'][:8]
        print(f"  {run['name']:<25} {sha} {run['status']:<10} {run['conclusion'] or '-':<10} {run['created_at']}")
except Exception as e:
    print('  error:', e)

print('\n=== Live ad slot count ===')
for u in ['/', '/pals/', '/breeding/', '/tech-tree/', '/about/', '/404']:
    try:
        req = urllib.request.Request(f'https://palworldpedia.cc{u}', headers={'User-Agent': 'Mozilla/5.0'})
        c = urllib.request.urlopen(req, timeout=15).read().decode('utf-8', 'ignore')
        ins = len(re.findall(r'<ins class="adsbygoogle"', c))
        print(f'  palworldpedia.cc{u:<15} ins={ins}')
    except Exception as e:
        print(f'  {u}: error {e}')
