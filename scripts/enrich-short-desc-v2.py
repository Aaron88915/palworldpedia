#!/usr/bin/env python3
"""
V2 enrichment for descriptions we filled this run.
Fixes punctuation and expands short (< 70 char) descriptions with category-aware
content to reach SEO-ideal length (70-155 chars).
Skips pre-existing short descriptions (out of scope for this task).
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TECH_JSON = ROOT / 'src' / 'data' / 'tech.json'
CACHE = ROOT / 'scripts' / 'paldb-tech-desc-cache.json'

IDEAL_MIN = 70
IDEAL_MAX = 155

cache = json.loads(CACHE.read_text(encoding='utf-8'))
mine = set(cache.keys())

techs = json.loads(TECH_JSON.read_text(encoding='utf-8'))

def split_first_period(s):
    """Split description into first sentence and rest, by the FIRST period followed by space/end."""
    s = s.strip()
    m = re.search(r'\.\s', s)
    if m:
        first = s[:m.end()].strip()  # includes period and trailing space
        rest = s[m.end():].strip()
    else:
        first = s
        rest = ''
    return first, rest

def expand_saddle(tech, first, rest, cost):
    """For SkillUnlock_* saddles: 'Saddle for safely riding X.'"""
    # Extract Pal name from existing 'Saddle for safely riding X.'
    m = re.match(r'Saddle for safely riding (.+?)\.?\s*$', first, re.I)
    pal = m.group(1).strip() if m else tech['name']
    # Build a richer description
    parts = [f"Saddle for safely riding {pal}."]
    parts.append(" Equip on the Pal to ride it and activate its Partner Skill in combat and travel.")
    parts.append(f" Unlocks at level {cost}.")
    out = "".join(parts)
    return cap(out, IDEAL_MAX)

def expand_statue(tech, first, rest, cost):
    """For decorative statues like IceHorseStatue."""
    # first might be 'Decorative Frostallion statue.'
    parts = [first.rstrip('.') + "."]
    parts.append(" Place it in your base to add visual flair to your Palworld home.")
    parts.append(f" Unlocks at level {cost}.")
    out = "".join(parts)
    return cap(out, IDEAL_MAX)

def expand_wing_fuel(tech, first, rest, cost):
    """WingGlider_Fuel."""
    parts = ["The fuel required to power the Wing Pack."]
    parts.append(" Craft to refill your glider's fuel reserves for extended aerial travel.")
    parts.append(f" Unlocks at level {cost}.")
    out = "".join(parts)
    return cap(out, IDEAL_MAX)

def expand_generic(tech, first, rest, cost):
    """Generic enrichment: add a 'Use this for ...' sentence and unlock info."""
    parts = [first]
    cat = tech.get('category', 'Items')
    if cat == 'Structures':
        # Already have first sentence; just append unlock
        pass
    if rest:
        parts.append(" " + rest)
    if not any('unlock' in p.lower() or 'level' in p.lower() for p in parts):
        parts.append(f" Unlocks at level {cost}.")
    out = "".join(parts)
    out = cap(out, IDEAL_MAX)
    if len(out) < IDEAL_MIN:
        # Try appending a "see full stats" call-to-action
        extra = " See full stats and required materials on the detail page."
        out = (out.rstrip('. ') + extra).strip()
        out = cap(out, IDEAL_MAX)
    return out

def cap(s, n):
    s = re.sub(r'\s+', ' ', s).strip()
    if len(s) > n:
        s = s[:n - 1].rstrip(' ,;:.-') + '\u2026'
    return s

def fix_punctuation(s):
    """Ensure each sentence ends with a period."""
    s = re.sub(r'\s+', ' ', s).strip()
    # If has ' Unlocks at level' but no period before it, insert one
    s = re.sub(r'([a-z])\s+(?=Unlocks at level)', r'\1. ', s, flags=re.I)
    if not s.endswith(('.', '!', '?', '\u2026')):
        s += '.'
    return s

changed = 0
for t in techs:
    if t['slug'] not in mine:
        continue
    desc = (t.get('description') or '').strip()
    if not desc:
        continue
    if len(desc) >= IDEAL_MIN:
        # Still fix punctuation
        fixed = fix_punctuation(desc)
        if fixed != desc:
            t['description'] = fixed
            changed += 1
        continue
    # Short: fix and expand
    desc = fix_punctuation(desc)
    first, rest = split_first_period(desc)
    cost = t.get('cost', 0)
    slug = t['slug']
    name = t['name']
    cat = t.get('category', 'Items')
    if slug.startswith('SkillUnlock_') and 'Saddle for safely riding' in first:
        new = expand_saddle(t, first, rest, cost)
    elif 'Statue' in name or 'statue' in first:
        new = expand_statue(t, first, rest, cost)
    elif slug == 'WingGlider_Fuel':
        new = expand_wing_fuel(t, first, rest, cost)
    else:
        new = expand_generic(t, first, rest, cost)
    new = cap(new, IDEAL_MAX)
    if new != desc and len(new) >= len(desc):
        t['description'] = new
        changed += 1

TECH_JSON.write_text(json.dumps(techs, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'Changed: {changed}')

# Re-audit
def desc(t): return (t.get('description') or '').strip()
empty = [t for t in techs if len(desc(t)) < 30]
short = [t for t in techs if 0 < len(desc(t)) < 70]
ideal = [t for t in techs if 70 <= len(desc(t)) <= 155]
long_ = [t for t in techs if 155 < len(desc(t)) < 200]
toolong = [t for t in techs if len(desc(t)) >= 200]
print()
print(f'After v2 enrichment:')
print(f'  Empty (<30): {len(empty)}')
print(f'  Short (30-70): {len(short)}')
print(f'  Ideal (70-155): {len(ideal)}')
print(f'  Long (155-200): {len(long_)}')
print(f'  Too long (>=200): {len(toolong)}')

# Show still-short mine
mine_short = [t for t in short if t['slug'] in mine]
print()
print(f'My techs still short: {len(mine_short)}')
for t in mine_short:
    print(' ', f'{t["slug"]:40}', '|', desc(t))
