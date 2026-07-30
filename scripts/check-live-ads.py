#!/usr/bin/env python3
"""检查线上 palworldpedia.cc 部署状态"""
import urllib.request
import re
import json

print('=== 线上广告位检查 ===')
urls = [
    'https://palworldpedia.cc/',
    'https://palworldpedia.cc/pals/',
    'https://palworldpedia.cc/breeding/',
    'https://palworldpedia.cc/tech-tree/',
    'https://palworldpedia.cc/about/',
    'https://palworldpedia.cc/contact/',
    'https://palworldpedia.cc/privacy/',
    'https://palworldpedia.cc/terms/',
    'https://palworldpedia.cc/404',
]
for u in urls:
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
        r = urllib.request.urlopen(req, timeout=15)
        c = r.read().decode('utf-8', 'ignore')
        ins_count = len(re.findall(r'<ins class="adsbygoogle"', c))
        title_match = re.search(r'<title>([^<]+)</title>', c)
        title = title_match.group(1) if title_match else ''
        print(f'{u:<48} {r.status} ins={ins_count}  {title[:50]}')
    except Exception as e:
        print(f'{u:<48} ERROR: {e}')

print()
print('=== GitHub Actions 最近构建 ===')
try:
    req = urllib.request.Request(
        'https://api.github.com/repos/Aaron88915/palworldpedia/actions/runs?per_page=3',
        headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/vnd.github+json'},
    )
    data = json.loads(urllib.request.urlopen(req, timeout=15).read().decode('utf-8'))
    for run in data.get('workflow_runs', []):
        sha = run['head_sha'][:8]
        name = run['name']
        status = run['status']
        conclusion = run['conclusion'] or '-'
        created = run['created_at']
        print(f'{name:<20} {sha} {status:<10} {conclusion:<10} {created}')
except Exception as e:
    print('gh api error:', e)
