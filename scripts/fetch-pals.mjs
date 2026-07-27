/**
 * Palworld 帕鲁数据抓取脚本 (v2 - 并发 + 增量)
 *
 * 数据源: Fandom Wiki API (palworld.fandom.com)
 * 协议: CC-BY-SA 4.0 (二次加工 + 标注来源)
 *
 * 使用:
 *   node scripts/fetch-pals.mjs
 *
 * 输出: src/data/pals.json
 * 进度: src/data/pals.progress.json (断点续抓)
 */

import { writeFile, readFile, mkdir } from 'fs/promises';
import { existsSync } from 'fs';

const API = 'https://palworld.fandom.com/api.php';
const USER_AGENT = 'Palworldpedia-Bot/1.0 (https://palworldpedia.cc) Node.js';
const CONCURRENCY = 8;          // 并发数
const RATE_LIMIT_MS = 100;      // 每个 worker 间隔
const OUTPUT_PATH = 'src/data/pals.json';
const PROGRESS_PATH = 'src/data/pals.progress.json';

// 类型映射
const TYPE_MAP = {
  Neutral: 'neutral', Fire: 'fire', Water: 'water', Grass: 'grass',
  Electric: 'electric', Ice: 'ice', Ground: 'ground', Dark: 'dark', Dragon: 'dragon',
};
const WORK_FIELDS = [
  'handiwork', 'transporting', 'farming', 'kindling', 'watering',
  'planting', 'lumbering', 'mining', 'generating_electricity',
  'medicine_production', 'cooling', 'gathering',
];

let progressCounter = { ok: 0, fail: 0 };

async function apiFetch(params, retries = 2) {
  const url = new URL(API);
  for (const [k, v] of Object.entries(params)) url.searchParams.set(k, v);
  for (let i = 0; i <= retries; i++) {
    try {
      const res = await fetch(url, { headers: { 'User-Agent': USER_AGENT } });
      if (res.status === 429 || res.status === 503) {
        await new Promise((r) => setTimeout(r, 1500 * (i + 1)));
        continue;
      }
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.json();
    } catch (e) {
      if (i === retries) throw e;
      await new Promise((r) => setTimeout(r, 800 * (i + 1)));
    }
  }
}

async function listAllPals() {
  const pals = [];
  let cmcontinue = null;
  do {
    const data = await apiFetch({
      action: 'query',
      list: 'categorymembers',
      cmtitle: 'Category:Pals',
      cmlimit: '500',
      cmnamespace: '0',
      format: 'json',
      ...(cmcontinue ? { cmcontinue } : {}),
    });
    pals.push(...(data.query?.categorymembers || []));
    cmcontinue = data.continue?.cmcontinue;
  } while (cmcontinue);
  return pals;
}

async function fetchPalWikitext(title) {
  const data = await apiFetch({
    action: 'parse', page: title, prop: 'wikitext', format: 'json',
  });
  return data.parse?.wikitext?.['*'] || '';
}

function parsePalTemplate(wt) {
  const m = wt.match(/\{\{Pal\n([\s\S]+?)\n\}\}/);
  if (!m) return null;
  const fields = {};
  for (const line of m[1].split('\n')) {
    const f = line.match(/^\|\s*([\w_]+)\s*=\s*(.*?)\s*$/);
    if (f) fields[f[1]] = f[2].trim();
  }
  return fields;
}

function parsePalTableStats(wt) {
  const m = wt.match(/\{\{Pal Table Stats\n([\s\S]+?)\n\}\}/);
  if (!m) return null;
  const fields = {};
  for (const line of m[1].split('\n')) {
    const f = line.match(/^\|\s*([\w_]+)\s*=\s*(.*?)\s*$/);
    if (f) fields[f[1]] = f[2].trim();
  }
  return fields;
}

function parseSkills(wt) {
  const skills = [];
  const re = /\{\{PalSkillListEntry\+\|([^|}]+)\|level=(\d+)\}\}/g;
  let m;
  while ((m = re.exec(wt)) !== null) {
    skills.push({ name: m[1].trim(), level: parseInt(m[2], 10) });
  }
  return skills;
}

function parseDescription(wt) {
  const m = wt.match(/==\s*Palpedia Entry\s*==\s*\{\{Paldeck\|([\s\S]+?)\}\}/);
  return m ? m[1].trim().replace(/\s+/g, ' ') : '';
}

function parseWorkSuitability(fields) {
  const w = {};
  for (const k of WORK_FIELDS) {
    const v = parseInt(fields[k], 10);
    if (v > 0) w[k] = v;
  }
  return w;
}

function parseBiomes(wt) {
  const m = wt.match(/===\s*Wild Spawn\s*===\s*([\s\S]+?)(?====|$)/);
  if (!m) return [];
  const biomes = [];
  const seen = new Set();
  for (const line of m[1].split('\n')) {
    const lm = line.match(/\[\[([^\]|]+?)(?:\|[^\]]+)?\]\]/);
    if (lm && !seen.has(lm[1])) { seen.add(lm[1]); biomes.push(lm[1]); }
  }
  return biomes.slice(0, 8);
}

function parseDrops(wt) {
  const drops = [];
  const re = /\{\{i\|([^}|]+?)\}\}/g;
  let m;
  const seen = new Set();
  while ((m = re.exec(wt)) !== null) {
    const n = m[1].trim();
    if (!seen.has(n)) { seen.add(n); drops.push(n); }
  }
  return drops.slice(0, 12);
}

function slugify(name) {
  return name.toLowerCase().replace(/['']/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
}

/**
 * 并发抓取
 */
async function fetchAll(items, processor, concurrency, rateLimitMs) {
  const results = [];
  const queue = [...items];
  const inFlight = new Set();

  async function worker() {
    while (queue.length > 0) {
      const item = queue.shift();
      if (!item) break;
      try {
        const r = await processor(item);
        if (r) results.push(r);
      } catch (e) {
        progressCounter.fail++;
        process.stdout.write(`  ❌ ${item.title || item.id}: ${e.message}\n`);
      }
      await new Promise((res) => setTimeout(res, rateLimitMs));
    }
  }

  const workers = Array(concurrency).fill(null).map(worker);
  await Promise.all(workers);
  return results;
}

/**
 * 主流程
 */
async function main() {
  console.log('🚀 Palworld 帕鲁数据抓取 (并发模式)\n');

  // 加载已有进度（断点续抓）
  let pals = [];
  if (existsSync(PROGRESS_PATH)) {
    pals = JSON.parse(await readFile(PROGRESS_PATH, 'utf-8'));
    console.log(`  📂 加载已有进度: ${pals.length} 只帕鲁`);
  }

  // 列表
  console.log('📋 [1/3] 抓取帕鲁列表...');
  const list = await listAllPals();
  const filtered = list.filter((m) =>
    !['Pals', 'Alpha Pals', 'Lucky Pals', 'Predator Pals'].includes(m.title)
  );
  console.log(`  ✅ 共 ${list.length} 条目，过滤后 ${filtered.length} 只\n`);

  // 跳过已抓
  const existingIds = new Set(pals.map((p) => p.id));
  const toFetch = filtered.filter((m) => !existingIds.has(slugify(m.title)));
  console.log(`  🔄 待抓: ${toFetch.length}（已抓 ${existingIds.size}）\n`);

  if (toFetch.length === 0) {
    console.log('✨ 已全部抓取，跳过');
  } else {
    // 抓详情
    console.log(`📥 [2/3] 并发抓取详情（并发 ${CONCURRENCY}）...`);

    let lastSave = 0;
    await fetchAll(toFetch, async (item) => {
      const wt = await fetchPalWikitext(item.title);
      const fields = parsePalTemplate(wt);
      if (!fields) return null;
      const stats = parsePalTableStats(wt);
      const skills = parseSkills(wt);
      const desc = parseDescription(wt);
      const ws = parseWorkSuitability(fields);
      const biomes = parseBiomes(wt);
      const drops = parseDrops(wt);

      const palName = fields.name || item.title;
      const types = [TYPE_MAP[fields.ele1] || 'neutral'];
      if (fields.ele2 && TYPE_MAP[fields.ele2]) types.push(TYPE_MAP[fields.ele2]);

      const pal = {
        id: slugify(palName),
        paldeckNo: parseInt(fields.no, 10) || 0,
        name: { zh: palName, en: palName },
        types,
        rarity: 3,
        stats: {
          hp: parseInt(stats?.hp, 10) || 0,
          attack: { melee: parseInt(stats?.attack, 10) || 0, ranged: 0 },
          defense: parseInt(stats?.defense, 10) || 0,
          speed: 0,
        },
        workSuitability: ws,
        skills: skills.map((s) => ({
          id: slugify(s.name),
          name: { zh: s.name, en: s.name },
          level: s.level,
          type: types[0],
          power: 0, cooldown: 0,
          description: { zh: '', en: '' },
        })),
        passives: fields.partnerskill
          ? [{
              id: slugify(fields.partnerskill),
              name: { zh: fields.partnerskill, en: fields.partnerskill },
              description: { zh: fields.psdesc || '', en: fields.psdesc || '' },
            }]
          : [],
        drops,
        food: parseInt(fields.food, 10) || 0,
        price: 0,
        biomes,
        nightOnly: false,
        description: { zh: desc, en: desc },
        image: fields.image ? `/images/pals/${fields.image}` : '',
        breedpower: parseInt(fields.breedpower, 10) || 0,
        updatedAt: new Date().toISOString().split('T')[0],
      };

      progressCounter.ok++;
      pals.push(pal);

      // 每 30 个保存一次
      if (pals.length - lastSave >= 30) {
        lastSave = pals.length;
        await writeFile(PROGRESS_PATH, JSON.stringify(pals, null, 2));
        process.stdout.write(`  💾 [${pals.length}/${filtered.length}] 已保存进度\n`);
      }
      return pal;
    }, CONCURRENCY, RATE_LIMIT_MS);
  }

  // 排序 + 写入
  console.log(`\n💾 [3/3] 写入最终文件...`);
  pals.sort((a, b) => a.paldeckNo - b.paldeckNo);

  if (!existsSync('src/data')) await mkdir('src/data', { recursive: true });
  await writeFile(OUTPUT_PATH, JSON.stringify(pals, null, 2) + '\n', 'utf-8');
  console.log(`  ✅ ${pals.length} 只帕鲁 → ${OUTPUT_PATH}`);

  console.log(`\n🎉 完成!成功 ${progressCounter.ok} / 失败 ${progressCounter.fail}`);
}

main().catch((e) => { console.error('\n💥 失败:', e); process.exit(1); });
