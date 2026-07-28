# -*- coding: utf-8 -*-
"""Investigate BFS reachability - check if starters can reach Jetragon."""
import json
from collections import deque, Counter

with open('public/pals-data.json', 'r', encoding='utf-8') as f:
    pals = json.load(f)
with open('public/breeding-data.json', 'r', encoding='utf-8') as f:
    edges = json.load(f)

idx_to_id = [p['id'] for p in pals]
id_to_idx = {p['id']: i for i, p in enumerate(pals)}

# Forward: parent -> children
adj = {}
for i1, i2, c in edges:
    for x in (i1, i2):
        if x not in adj:
            adj[x] = set()
        adj[x].add(c)

# Reverse: child -> parents
reverse = {}
for i1, i2, c in edges:
    if c not in reverse:
        reverse[c] = []
    reverse[c].append((i1, i2))

# BFS from lamball
def bfs_reachable(source_ids, max_steps=20):
    sources = [id_to_idx[s] for s in source_ids if s in id_to_idx]
    visited = set(sources)
    queue = deque([(s, 0) for s in sources])
    max_depth = 0
    while queue:
        node, depth = queue.popleft()
        max_depth = max(max_depth, depth)
        if depth >= max_steps:
            continue
        for nxt in adj.get(node, []):
            if nxt in visited:
                continue
            visited.add(nxt)
            queue.append((nxt, depth + 1))
    return visited, max_depth

# What can lamball + cattiva + lifmunk + foxparks reach?
print('=== Reachability from common starters ===')
common = ['lamball', 'cattiva', 'lifmunk', 'foxparks', 'hoocrates', 'teafant', 'pengullet']
reached, depth = bfs_reachable(common, 15)
print(f'  Pals reached: {len(reached)} / {len(pals)}')
print(f'  Max BFS depth: {depth}')

# What are the unreachable?
unreached = [p for p in pals if id_to_idx[p['id']] not in reached]
print(f'  Unreachable: {len(unreached)}')
print('  Sample unreachable (first 30):')
for p in unreached[:30]:
    print(f'    {p["zh"]} ({p["id"]})')

# Check legendary specifically
print('\n=== Can we reach any legendary? ===')
legendary = ['jetragon', 'frostallion', 'paladius', 'necromus', 'neptilius', 'bellanoir', 'frostallion-noct', 'bellanoir-libero']
for lid in legendary:
    if lid in id_to_idx:
        idx = id_to_idx[lid]
        in_set = idx in reached
        print(f'  {lid}: {"YES" if in_set else "NO"} (idx={idx})')

# How many steps to Jetragon specifically?
def bfs_path(source_ids, target_id):
    sources = [id_to_idx[s] for s in source_ids if s in id_to_idx]
    target = id_to_idx.get(target_id)
    if target is None or not sources:
        return None
    if target in sources:
        return [target]
    visited = {s: None for s in sources}
    queue = deque(sources)
    while queue:
        node = queue.popleft()
        for nxt in adj.get(node, []):
            if nxt in visited:
                continue
            visited[nxt] = node
            if nxt == target:
                path = [target]
                while path[-1] is not None:
                    p = visited[path[-1]]
                    if p is None:
                        break
                    path.append(p)
                path.reverse()
                return path
            queue.append(nxt)
    return None

print('\n=== BFS path tests ===')
for target in ['jetragon', 'frostallion', 'mau', 'wixen', 'anubis']:
    path = bfs_path(common, target)
    if path:
        print(f'  -> {target}: {len(path)-1} steps, {" -> ".join(idx_to_id[i] for i in path)}')
    else:
        print(f'  -> {target}: NO PATH from {len(common)} common starters')
