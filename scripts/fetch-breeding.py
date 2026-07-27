"""
Palworld 配种数据抓取 (Python)
数据源: Fandom Wiki
输出: src/data/breeding.json
"""
import urllib.request
import urllib.parse
import json
import re
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

ROOT = r'D:\minamax\projects\palworldpedia'
PAL_FILE = os.path.join(ROOT, 'src', 'data', 'pals.json')
OUT_FILE = os.path.join(ROOT, 'src', 'data', 'breeding.json')
UA = 'Mozilla/5.0 (Palworldpedia-Bot/1.0)'

def fetch_html(title):
    url = f'https://palworld.fandom.com/api.php?action=parse&page={urllib.parse.quote(title)}&prop=text&format=json'
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode('utf-8'))

def parse_breeding_edges(html, child_id):
    """从帕鲁 HTML 提取配种边 (parent1, parent2, child)"""
    # 找 Breeding 段
    breed_idx = html.find('id="Breeding"')
    if breed_idx < 0:
        return []
    # 找下一个 h2/h3 段结束（不能用 id="，因为 UI 组件有 id）
    next_idx = len(html)
    for tag in ['<h2', '<h3']:
        i = html.find(tag, breed_idx + 10)
        if 0 < i < next_idx:
            next_idx = i
    if next_idx > len(html) - 10:
        next_idx = breed_idx + 12000
    block = html[breed_idx:next_idx]
    # 找 mw-collapsible-content
    coll = block.find('mw-collapsible-content')
    if coll < 0:
        return []
    block = block[coll:]
    # 按 <br /> 切分行
    rows = block.split('<br />')
    edges = []
    for row in rows:
        # 找所有 /wiki/X 引用
        refs = re.findall(r'href="/wiki/([^"/]+)"', row)
        if len(refs) >= 2:
            p1, p2 = refs[0], refs[1]
            # 跳过含特殊字符（子分类）
            if any(c in p1 for c in '():') or any(c in p2 for c in '():'):
                continue
            edges.append({'parent1': p1, 'parent2': p2, 'child': child_id})
    return edges

def main():
    with open(PAL_FILE, 'r', encoding='utf-8') as f:
        pals = json.load(f)
    print(f'帕鲁总数: {len(pals)}')

    # 加载已有
    existing = []
    if os.path.exists(OUT_FILE):
        with open(OUT_FILE, 'r', encoding='utf-8') as f:
            existing = json.load(f)
        print(f'已有 {len(existing)} 条边')
    existing_map = {e['child'] for e in existing if e.get('child')}

    to_fetch = [p for p in pals if p.get('paldeckNo', 0) > 0 and p['id'] not in existing_map]
    print(f'待抓: {len(to_fetch)}')

    new_edges = []
    ok = fail = 0
    lock = Lock()
    start = time.time()

    def worker(pal):
        nonlocal ok, fail
        title = pal['name']['en']
        slug = pal['id']
        try:
            data = fetch_html(title)
            html = data.get('parse', {}).get('text', {}).get('*', '')
            if not html:
                raise ValueError('empty html')
            edges = parse_breeding_edges(html, slug)
            with lock:
                nonlocal_ok = ok
                new_edges.extend(edges)
                ok += 1
            return (slug, len(edges))
        except Exception as e:
            with lock:
                fail += 1
            return (slug, 0, str(e))

    # 8 并发
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = {pool.submit(worker, p): p for p in to_fetch}
        for i, fut in enumerate(as_completed(futures)):
            r = fut.result()
            if (i + 1) % 30 == 0:
                elapsed = time.time() - start
                rate = (i + 1) / elapsed if elapsed > 0 else 0
                print(f'[{i+1}/{len(to_fetch)}] OK={ok} FAIL={fail} edges={len(new_edges)} ({rate:.1f}/s)')

    # 合并去重
    all_edges = existing + new_edges
    seen = set()
    unique = []
    for e in all_edges:
        k = f"{e['parent1']}|{e['parent2']}|{e['child']}"
        if k not in seen:
            seen.add(k)
            unique.append(e)
    unique.sort(key=lambda e: (e['child'], e['parent1'], e['parent2']))

    with open(OUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(unique, f, ensure_ascii=False, indent=2)

    elapsed = time.time() - start
    print(f'\n✅ 完成: 成功 {ok} / 失败 {fail}')
    print(f'总边数: {len(unique)}')
    print(f'耗时: {elapsed:.0f}s')

if __name__ == '__main__':
    main()
