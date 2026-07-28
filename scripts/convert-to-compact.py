# -*- coding: utf-8 -*-
"""Convert verbose breeding data to compact [i1, i2, c_idx] format for the page."""
import json

pals = json.load(open('public/pals-data.json', encoding='utf-8'))
edges = json.load(open('public/breeding-data.json', encoding='utf-8'))

id_to_idx = {p['id']: i for i, p in enumerate(pals)}

compact = []
unmapped = 0
for e in edges:
    i1 = id_to_idx.get(e['p1'])
    i2 = id_to_idx.get(e['p2'])
    c = id_to_idx.get(e['c'])
    if i1 is None or i2 is None or c is None:
        unmapped += 1
        continue
    compact.append([i1, i2, c])

print(f'Total edges: {len(edges)}, compact: {len(compact)}, unmapped: {unmapped}')
print(f'Sample: {compact[:3]}')

# Save as compact array
with open('public/breeding-data.json', 'w', encoding='utf-8') as f:
    json.dump(compact, f, ensure_ascii=False, separators=(',', ':'))

import os
size = os.path.getsize('public/breeding-data.json')
print(f'Saved compact: {size/1024:.1f} KB')

# Test BFS reachability now
from collections import deque
adj = {}
for i1, i2, c in compact:
    if i1 not in adj: adj[i1] = set()
    if i2 not in adj: adj[i2] = set()
    adj[i1].add(c)
    adj[i2].add(c)

sources = ['lamball', 'cattiva', 'lifmunk', 'foxparks', 'hoocrates', 'teafant', 'pengullet']
src_idxs = [id_to_idx[s] for s in sources]
target = id_to_idx['grizzbolt']

# BFS
visited = {s: None for s in src_idxs}
queue = deque(src_idxs)
found = None
while queue:
    node = queue.popleft()
    for nxt in adj.get(node, []):
        if nxt in visited:
            continue
        visited[nxt] = node
        if nxt == target:
            found = nxt
            break
        queue.append(nxt)
    if found:
        break

if found is not None:
    # Reconstruct path
    path = [found]
    while path[-1] is not None:
        p = visited[path[-1]]
        if p is None: break
        path.append(p)
    path.reverse()
    print(f'\nPath to Grizzbolt: {" -> ".join(pals[i]["id"] for i in path)} ({len(path)-1} steps)')
else:
    print('\nNo path to Grizzbolt')

# Try legendary
target = id_to_idx['jetragon']
visited = {s: None for s in src_idxs}
queue = deque(src_idxs)
found = None
while queue:
    node = queue.popleft()
    for nxt in adj.get(node, []):
        if nxt in visited:
            continue
        visited[nxt] = node
        if nxt == target:
            found = nxt
            break
        queue.append(nxt)
    if found: break
print(f'Jetragon reachable from starters: {found is not None}')

# Orserk
target = id_to_idx['orserk']
visited = {s: None for s in src_idxs}
queue = deque(src_idxs)
found = None
while queue:
    node = queue.popleft()
    for nxt in adj.get(node, []):
        if nxt in visited:
            continue
        visited[nxt] = node
        if nxt == target:
            found = nxt
            break
        queue.append(nxt)
    if found: break
if found is not None:
    path = [found]
    while path[-1] is not None:
        p = visited[path[-1]]
        if p is None: break
        path.append(p)
    path.reverse()
    print(f'Path to Orserk: {" -> ".join(pals[i]["id"] for i in path)} ({len(path)-1} steps)')
else:
    print('No path to Orserk')
