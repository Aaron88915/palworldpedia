#!/usr/bin/env python3
"""
Update PalImage component to show graceful fallback when image fails.
Also rebuild breeding-data.json with the new pal indices (after 7 stubs removed).
"""
import json
import csv
from pathlib import Path

ROOT = Path(__file__).parent.parent
PALS_JSON = ROOT / 'src' / 'data' / 'pals.json'
PALS_DATA = ROOT / 'public' / 'pals-data.json'
BREED_DATA = ROOT / 'public' / 'breeding-data.json'
PAL_IMAGE = ROOT / 'src' / 'components' / 'PalImage.astro'
RAW_DIR = ROOT / 'scripts'

# Load our pals (now 288 after stub removal)
with open(PALS_JSON, 'r', encoding='utf-8') as f:
    pals = json.load(f)
print(f'Loaded {len(pals)} pals')

# Save compact version
compact = [
    {
        'id': p['id'],
        'zh': p['name']['zh'],
        'en': p['name']['en'],
        'types': p['types'],
        'img': p['image'],
    }
    for p in pals
]
with open(PALS_DATA, 'w', encoding='utf-8') as f:
    json.dump(compact, f, ensure_ascii=False, separators=(',', ':'))
print(f'Wrote {PALS_DATA}')

# Rebuild breeding edges from becker AllCombos.csv
# Build name -> index lookup
name_to_idx = {}
for i, p in enumerate(compact):
    name_to_idx[p['en'].lower()] = i
    name_to_idx[p['id'].lower()] = i

# Load becker roster + matrix
with open(RAW_DIR / 'raw-beckerfelipee-Pals.csv', 'r', encoding='utf-8-sig') as f:
    roster = [line.strip() for line in f if line.strip()]
with open(RAW_DIR / 'raw-beckerfelipee-AllCombos.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.reader(f, delimiter=';')
    matrix = list(reader)

print(f'Becker matrix: {len(matrix)}x{len(roster)}')

# Build edges
edges = []
unmapped = 0
for row in range(len(roster)):
    if len(matrix[row]) != len(roster):
        continue
    p1_name = roster[row]
    p1_idx = name_to_idx.get(p1_name.lower())
    if p1_idx is None:
        unmapped += 1
        continue
    for col in range(row, len(roster)):
        p2_name = roster[col]
        p2_idx = name_to_idx.get(p2_name.lower())
        child_name = matrix[row][col]
        child_idx = name_to_idx.get(child_name.lower())
        if p2_idx is None or child_idx is None:
            unmapped += 1
            continue
        a, b = sorted([p1_idx, p2_idx])
        edges.append([a, b, child_idx])

# Dedupe
unique_edges = list({tuple(e): e for e in edges}.values())
unique_edges.sort()
print(f'Edges: {len(unique_edges)} (unmapped: {unmapped})')

# Save
with open(BREED_DATA, 'w', encoding='utf-8') as f:
    json.dump(unique_edges, f, ensure_ascii=False, separators=(',', ':'))
print(f'Wrote {BREED_DATA}')

# Also update PalImage component to show graceful fallback
pal_image = PAL_IMAGE.read_text(encoding='utf-8')
print(f'\nCurrent PalImage.astro ({len(pal_image)} bytes):')
print(pal_image[:500])

# Check if it has onerror handling
if 'onerror' not in pal_image.lower():
    print('\n⚠ No onerror handler - adding fallback')

    # Add a CSS-based fallback: when image errors, show a colored div with type icon + name initial
    new_fallback = '''---
import type { Pal } from '@data/types';
interface Props {
  pal: Pal;
  size?: 'small' | 'medium' | 'large';
  rounded?: boolean;
  class?: string;
}
const { pal, size = 'medium', rounded = false, class: className = '' } = Astro.props;
const sizeClass = size === 'small' ? 'pal-image-small' : size === 'large' ? 'pal-image-large' : 'pal-image-medium';
const roundedClass = rounded ? 'rounded' : '';
// Type-based color for fallback
const typeColors: Record<string, string> = {
  normal: '#9ca3af', fire: '#ef4444', water: '#3b82f6', grass: '#22c55e',
  electric: '#eab308', ice: '#67e8f9', ground: '#a16207', dark: '#6b21a8',
  dragon: '#7c3aed', light: '#fde047', neutral: '#9ca3af',
};
const primaryType = pal.types[0] || 'normal';
const bgColor = typeColors[primaryType] || typeColors.normal;
const initial = (pal.name?.zh || pal.name?.en || '?').charAt(0);
---

<div class:list={['pal-image-wrap', sizeClass, roundedClass, className]} style={`--pal-bg: ${bgColor}`} data-pal-id={pal.id}>
  <img
    src={pal.image}
    alt={pal.name?.zh || pal.name?.en || 'pal'}
    class="pal-image"
    loading="lazy"
    decoding="async"
    onerror="this.onerror=null; this.style.display='none'; this.nextElementSibling.style.display='flex';"
  />
  <div class="pal-image-fallback" style="display: none;">
    <span style="color: white; font-weight: 800; font-size: 2em; text-shadow: 0 2px 4px rgba(0,0,0,0.3);">{initial}</span>
  </div>
</div>

<style>
  .pal-image-wrap {
    width: 100%;
    aspect-ratio: 1;
    background: linear-gradient(135deg, var(--bg-tertiary), var(--bg-secondary));
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
  }
  .pal-image-wrap.rounded { border-radius: var(--radius); }
  .pal-image {
    width: 100%;
    height: 100%;
    object-fit: contain;
    image-rendering: -webkit-optimize-contrast;
  }
  .pal-image-fallback {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--pal-bg, #6b7280);
    background: linear-gradient(135deg, var(--pal-bg, #6b7280), color-mix(in srgb, var(--pal-bg) 70%, black));
  }
  .pal-image-fallback span {
    font-size: 3rem;
    line-height: 1;
  }
  .pal-image-small .pal-image-fallback span { font-size: 1.5rem; }
  .pal-image-large .pal-image-fallback span { font-size: 5rem; }
</style>
'''
    PAL_IMAGE.write_text(new_fallback, encoding='utf-8')
    print(f'\nUpdated {PAL_IMAGE} with image fallback')
else:
    print('\n✓ PalImage already has fallback handling')
