# -*- coding: utf-8 -*-
"""Test multi-source BFS algorithm in Python (mirror JS logic)."""
import json
from collections import deque

# Load
with open('public/pals-data.json', 'r', encoding='utf-8') as f:
    pals = json.load(f)
with open('public/breeding-data.json', 'r', encoding='utf-8') as f:
    edges = json.load(f)

# Build maps
idx_to_id = [p['id'] for p in pals]
id_to_idx = {p['id']: i for i, p in enumerate(pals)}
adj = {}  # parent_idx -> set of child_idx
reverse = {}  # child_idx -> list of (a, b)

for i1, i2, c in edges:
    for x in (i1, i2):
        if x not in adj:
            adj[x] = set()
        adj[x].add(c)
    if c not in reverse:
        reverse[c] = []
    reverse[c].append((i1, i2))

def multi_source_bfs(owned_ids, target_id):
    """Mirrors JS implementation."""
    target = id_to_idx.get(target_id)
    if target is None:
        return None
    sources = [id_to_idx[o] for o in owned_ids if o in id_to_idx]
    if not sources:
        return None
    if target in sources:
        return {'sourceIdx': target, 'path': [target]}

    visited = {}
    queue = deque()
    for s in sources:
        visited[s] = {'parent': None, 'sourceIdx': s}
        queue.append(s)

    found = None
    while queue:
        node = queue.popleft()
        if node == target:
            found = visited[target]
            break
        for nxt in adj.get(node, []):
            if nxt in visited:
                continue
            visited[nxt] = {'parent': node, 'sourceIdx': visited[node]['sourceIdx']}
            if nxt == target:
                found = visited[nxt]
                break
            queue.append(nxt)
        if found:
            break

    if not found:
        return None

    # Reconstruct path
    path = []
    cur = target
    while cur is not None:
        path.append(cur)
        info = visited.get(cur)
        if not info or info['parent'] is None:
            break
        cur = info['parent']
    path.reverse()
    return {'sourceIdx': found['sourceIdx'], 'path': path}


# Test 1: Frostallion from common starters
print('=== Test 1: Frostallion from starters ===')
owned = ['lamball', 'cattiva', 'lifmunk', 'foxparks', 'hoocrates', 'teafant',
         'pengullet', 'anubis', 'mau', 'grizzbolt', 'relaxaurus']
result = multi_source_bfs(owned, 'frostallion')
if result:
    p = result['path']
    print(f'  Found! Source: {idx_to_id[result["sourceIdx"]]} ({pals[id_to_idx[idx_to_id[result["sourceIdx"]]]]["zh"]})')
    print(f'  Path length: {len(p) - 1} steps')
    print(f'  Path: {" -> ".join(idx_to_id[i] for i in p)}')
else:
    print('  No path found')

# Test 2: Jetragon from minimal set
print('\n=== Test 2: Jetragon from minimal set ===')
owned = ['lamball', 'cattiva']
result = multi_source_bfs(owned, 'jetragon')
if result:
    p = result['path']
    print(f'  Found! Source: {idx_to_id[result["sourceIdx"]]}')
    print(f'  Path length: {len(p) - 1} steps')
    print(f'  Path: {" -> ".join(idx_to_id[i] for i in p)}')
else:
    print('  No path found')

# Test 3: Target is in owned
print('\n=== Test 3: Target in owned set ===')
owned = ['jetragon', 'lamball', 'cattiva']
result = multi_source_bfs(owned, 'jetragon')
print(f'  Result: {result}')

# Test 4: Common pal Mau
print('\n=== Test 4: Mau from starters ===')
owned = ['lamball', 'cattiva']
result = multi_source_bfs(owned, 'mau')
if result:
    p = result['path']
    print(f'  Source: {idx_to_id[result["sourceIdx"]]}, Steps: {len(p) - 1}')
    print(f'  Path: {" -> ".join(idx_to_id[i] for i in p)}')
