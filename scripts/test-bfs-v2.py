# -*- coding: utf-8 -*-
"""Test BFS with real data to verify Path Finder logic."""
import json
from collections import deque

pals = json.load(open('public/pals-data.json', encoding='utf-8'))
edges = json.load(open('public/breeding-data.json', encoding='utf-8'))
id_to_idx = {p['id']: i for i, p in enumerate(pals)}

# Build adj map
adj = {}
for i1, i2, c in edges:
    if i1 not in adj: adj[i1] = set()
    if i2 not in adj: adj[i2] = set()
    adj[i1].add(c)
    adj[i2].add(c)


def multi_source_bfs(owned_ids, target_id):
    sources = [id_to_idx[o] for o in owned_ids if o in id_to_idx]
    target = id_to_idx.get(target_id)
    if target is None: return None
    if not sources: return None
    if target in sources: return [target]
    visited = {s: None for s in sources}
    queue = deque(sources)
    while queue:
        node = queue.popleft()
        for nxt in adj.get(node, []):
            if nxt in visited: continue
            visited[nxt] = node
            if nxt == target:
                path = [target]
                while path[-1] is not None:
                    p = visited[path[-1]]
                    if p is None: break
                    path.append(p)
                path.reverse()
                return path
            queue.append(nxt)
    return None


# Test various targets
print('=== Multi-source BFS tests ===')
owned = ['lamball', 'cattiva', 'lifmunk', 'foxparks', 'hoocrates', 'teafant', 'pengullet']
print(f'Owned: {owned}\n')

tests = [
    ('mau', 'Common starter'),
    ('anubis', 'Epic with 234 recipes'),
    ('jormuntide', 'Epic with 210 recipes'),
    ('caprity', 'Common intermediate'),
    ('wixen', 'Common child'),
    ('grizzbolt', 'Self-only boss'),
    ('jetragon', 'Legendary (uncatchable?)'),
    ('flopie', 'Basic'),
]

for target, desc in tests:
    if target not in id_to_idx:
        print(f'  {target}: NOT IN DB')
        continue
    path = multi_source_bfs(owned, target)
    if path:
        names = [pals[i]['id'] for i in path]
        print(f'  {target} ({desc}): {len(path)-1} steps - {" -> ".join(names)}')
    else:
        print(f'  {target} ({desc}): NO PATH')

# Add a few more owned to see if we can reach Grizzbolt
print('\n=== Adding rare pals to owned set ===')
owned_plus = owned + ['caprity', 'anubis', 'mau-cryst', 'foxparks-cryst', 'melpaca']
for target, desc in tests:
    if target not in id_to_idx: continue
    path = multi_source_bfs(owned_plus, target)
    if path:
        names = [pals[i]['id'] for i in path]
        print(f'  {target}: {len(path)-1} steps - {" -> ".join(names)}')
    else:
        print(f'  {target}: NO PATH')
