# Tech Description Fill - Final Report

**Date:** 2026-08-03
**Project:** palworldpedia (Palworld 中文/英文 攻略站)
**Task:** Fill missing `description` for 104 tech nodes in `src/data/tech.json`

## Result

| Metric | Before | After |
|--------|--------|-------|
| Total techs | 587 | 587 |
| Missing/short description (< 30 chars) | 104 | **0** |
| Already filled | 483 | 587 |

Length distribution after fill:
- < 30 chars: **0**
- 30-70 chars: 20 (all pre-existing, out of scope; template auto-wraps to 100+ at render)
- 70-155 chars (SEO ideal): 151 (was 123, +28)
- 155-200 chars: 58
- ≥ 200 chars: 358 (pre-existing; template slices to 155 at render)

Build: `npm run build` ✓ — 1772 pages, no errors, ~50s.

## Sources of new descriptions

| Source | Count | Notes |
|--------|------:|-------|
| paldb.cc (`/en/{name}`) | 75 | Primary source. `og:description` meta tag. |
| Generated fallback | 29 | Mostly `FurnitureSet_*` (not on paldb). |
| wiki.gg | 0 | Slugs/names don't match; skipped. |

## Strategy

1. **Slug candidates per tech** (tried in order, first 200-OK wins):
   - `name.replace(' ', '_').replace("'", '')`
   - `name` URL-encoded
   - `slug` as-is
   - `slug` with underscores stripped
2. **Paldb fetch**: `GET https://paldb.cc/en/{slug}` with Chrome User-Agent, 0.35s sleep between requests, retries on 5xx.
3. **Wiki fallback**: lookup in `scripts/wikigg-tech-data.json` by lowercased name (only 4 of 104 matched, abandoned).
4. **Generated fallback**: category + name + cost-aware templates, e.g.:
   - `SkillUnlock_*` (saddle) → "Saddle for safely riding X. Equip on the Pal to ride it and activate its Partner Skill in combat and travel. Unlocks at level N."
   - `FurnitureSet_*` → "X is a decorative furniture set for base building. Unlocks at level N. Place to customize your Palworld base interior."
   - Etc.

5. **Refinement pass** (`enrich-short-desc-v2.py`): for paldb hits that came back < 70 chars and didn't mention unlock level, expanded with category-specific templates and re-capped at 155. 28 such fixes.

6. **Caching**: every paldb attempt cached in `scripts/paldb-tech-desc-cache.json` so re-runs skip the network.

## Files changed

- `M src/data/tech.json` — added 104 description fields (+206 / -105 lines, 311 net)
- `?? scripts/fill-tech-desc.py` — main fill script
- `?? scripts/enrich-short-desc-v2.py` — refinement pass (v1 deleted)
- `?? scripts/audit-data-gaps-en.py` — English-friendly audit (Chinese chars in original garbled in PowerShell)
- `?? scripts/paldb-tech-desc-cache.json` — paldb fetch cache
- `?? scripts/fill-tech-desc.log` — run log

## Out of scope (not touched)

- 20 pre-existing short descriptions (30-70 chars) — these were in the data before this task and not part of the 104. The `src/pages/en/tech-tree/[slug].astro` template auto-wraps them to 100+ chars at render, so they meet SEO on the live page.
- 358 pre-existing long descriptions (≥ 200 chars) — the template slices to 155 with ellipsis at render, so they don't hurt SEO. Truncating them in `tech.json` would lose data used by the detail body.
- Other `src/data/pals.json` biomes (10 → 7 missing, being handled by other agent).
