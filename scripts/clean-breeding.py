"""
清理 breeding.json:
1. Wiki 名字 → slug
2. 验证 parent/child 都在 pals.json 里
3. 保留所有边（含同种，Wiki 确认有效）
4. 统计报告
"""
import json
import os

ROOT = r'D:\minamax\projects\palworldpedia'
PAL_FILE = os.path.join(ROOT, 'src', 'data', 'pals.json')
OUT_FILE = os.path.join(ROOT, 'src', 'data', 'breeding.json')

def to_slug(name):
    """Wiki 名 → 我们的 slug. Blazehowl_Noct → blazehowl-noct"""
    return name.replace('_', ' ').lower().replace(' ', '-').replace("'", '').strip('-')

# 加载 pals
with open(PAL_FILE, 'r', encoding='utf-8') as f:
    pals = json.load(f)
pal_ids = {p['id'] for p in pals}
pal_by_id = {p['id']: p for p in pals}

# 加载边
with open(OUT_FILE, 'r', encoding='utf-8') as f:
    edges = json.load(f)
print(f'原始边数: {len(edges)}')

# 转换 + 验证
cleaned = []
seen = set()
skipped = 0
same_breed = 0
for e in edges:
    p1 = to_slug(e['parent1'])
    p2 = to_slug(e['parent2'])
    c = to_slug(e['child'])
    # 验证
    if p1 not in pal_ids or p2 not in pal_ids or c not in pal_ids:
        skipped += 1
        continue
    # 同种繁殖
    if p1 == c and p2 == c:
        same_breed += 1
    # 去重
    key = (p1, p2, c)
    if key in seen:
        continue
    seen.add(key)
    cleaned.append({'parent1': p1, 'parent2': p2, 'child': c})

cleaned.sort(key=lambda e: (e['child'], e['parent1'], e['parent2']))

with open(OUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(cleaned, f, ensure_ascii=False, indent=2)

print(f'清理后边数: {len(cleaned)}')
print(f'跳过（不在 pals.json）: {skipped}')
print(f'同种繁殖（X+X=X）: {same_breed}')
print(f'跨种配种: {len(cleaned) - same_breed}')

# 统计
unique_children = set(e['child'] for e in cleaned)
print(f'涉及帕鲁数: {len(unique_children)} / {len(pal_ids)}')

# 同种繁殖占比
if cleaned:
    same_pct = same_breed * 100 / len(cleaned)
    print(f'同种比例: {same_pct:.1f}%')
